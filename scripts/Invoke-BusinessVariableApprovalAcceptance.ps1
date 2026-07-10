param(
  [string]$Server = "root@47.94.159.60",
  [string]$BaseUrl = "https://heaotang.cn",
  [switch]$AllowMutatingTest
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

if (-not $AllowMutatingTest) { throw "Pass -AllowMutatingTest to approve the harmless 2099 capacity probe in the test database." }
if ($BaseUrl -ne "https://heaotang.cn" -or $Server -ne "root@47.94.159.60") { throw "This acceptance script is restricted to the approved test environment." }

function Get-HttpStatus([scriptblock]$Request) {
  try {
    & $Request | Out-Null
    return 200
  } catch {
    if ($_.Exception.Response) { return [int]$_.Exception.Response.StatusCode }
    throw
  }
}

function Get-TestIdentities {
  $remoteScript = @'
set -euo pipefail
phone=$(sqlite3 /root/heaotang-acceptance/runtime/data/heao.db "SELECT phone FROM users WHERE role >= 2 AND id <> 1 AND phone IS NOT NULL AND length(phone)=11 ORDER BY id LIMIT 1;")
password=$(sed -n 's/^export AUTH_ADMIN_PASSWORD=//p' /root/heaotang-acceptance/start-acceptance.sh | tail -n 1)
test -n "$phone"
test -n "$password"
printf 'PHONE=%s\n' "$phone"
printf 'PASSWORD=%s\n' "$password"
'@
  $inputPath = [IO.Path]::GetTempFileName()
  $outputPath = [IO.Path]::GetTempFileName()
  $stderrPath = [IO.Path]::GetTempFileName()
  try {
    [IO.File]::WriteAllText($inputPath, ($remoteScript -replace "`r", ""), (New-Object Text.UTF8Encoding($false)))
    $process = Start-Process ssh.exe `
      -ArgumentList @("-o", "BatchMode=yes", $Server, "bash", "-s") `
      -WindowStyle Hidden `
      -RedirectStandardInput $inputPath `
      -RedirectStandardOutput $outputPath `
      -RedirectStandardError $stderrPath `
      -Wait `
      -PassThru
    if ($process.ExitCode -ne 0) {
      throw "Unable to select existing test administrators: $([IO.File]::ReadAllText($stderrPath).Trim())"
    }
    $values = @{}
    foreach ($line in [IO.File]::ReadAllLines($outputPath)) {
      if ($line -match '^([A-Z]+)=(.+)$') { $values[$matches[1]] = $matches[2] }
    }
    if ([string]$values.PHONE -notmatch '^\d{11}$' -or -not [string]$values.PASSWORD) {
      throw "Test identity discovery did not return one phone administrator and the system administrator credential."
    }
    return [pscustomobject]@{ Phone = [string]$values.PHONE; AdminPassword = [string]$values.PASSWORD }
  } finally {
    Remove-Item -LiteralPath $inputPath, $outputPath, $stderrPath -Force -ErrorAction SilentlyContinue
  }
}

function New-TestSession([string]$Phone) {
  $sendCode = Invoke-RestMethod -Uri "$BaseUrl/api/v1/auth/send-code" -Method POST -ContentType "application/json" -Body (@{ phone = $Phone } | ConvertTo-Json -Compress)
  $code = [string]$sendCode.data.code
  if ($code -notmatch '^\d{6}$') { throw "Test environment did not return a development verification code." }
  $login = Invoke-RestMethod -Uri "$BaseUrl/api/v1/auth/login" -Method POST -ContentType "application/json" -Body (@{ phone = $Phone; code = $code } | ConvertTo-Json -Compress)
  $code = $null
  return [string]$login.data.token
}

function New-SystemAdminSession([string]$Password) {
  $login = Invoke-RestMethod -Uri "$BaseUrl/api/v1/auth/admin/login" -Method POST -ContentType "application/json" -Body (@{ username = "platform-admin"; password = $Password } | ConvertTo-Json -Compress)
  return [string]$login.token
}

$identities = Get-TestIdentities
$makerToken = New-TestSession $identities.Phone
$checkerToken = New-SystemAdminSession $identities.AdminPassword
$identities = $null
if (-not $makerToken -or -not $checkerToken) { throw "Unable to obtain both test administrator sessions." }

$probe = [DateTime]::UtcNow.ToString("yyyyMMddHHmmssfff")
$makerHeaders = @{ Authorization = "Bearer $makerToken"; "Idempotency-Key" = "capacity-probe-$probe" }
$proposal = Invoke-RestMethod `
  -Uri "$BaseUrl/api/v1/admin/business-variables/club.family.member_capacity" `
  -Method PUT `
  -Headers $makerHeaders `
  -ContentType "application/json" `
  -Body (@{ value = 20; effective_at = "2099-01-01T00:00:00Z"; reason = "automated maker-checker acceptance probe; no current behavior change" } | ConvertTo-Json -Compress)
$changeID = [int64]$proposal.data.id
if ($changeID -le 0 -or [string]$proposal.data.status -ne "pending") { throw "Proposal was not persisted as pending." }

$selfStatus = Get-HttpStatus {
  Invoke-RestMethod `
    -Uri "$BaseUrl/api/v1/admin/business-variable-changes/$changeID/review" `
    -Method POST `
    -Headers @{ Authorization = "Bearer $makerToken"; "Idempotency-Key" = "capacity-self-review-$probe" } `
    -ContentType "application/json" `
    -Body (@{ approved = $true; reason = "must be rejected" } | ConvertTo-Json -Compress)
}
if ($selfStatus -ne 403) { throw "Same-person review returned HTTP $selfStatus instead of 403." }

$approved = Invoke-RestMethod `
  -Uri "$BaseUrl/api/v1/admin/business-variable-changes/$changeID/review" `
  -Method POST `
  -Headers @{ Authorization = "Bearer $checkerToken"; "Idempotency-Key" = "capacity-checker-review-$probe" } `
  -ContentType "application/json" `
  -Body (@{ approved = $true; reason = "independent approval of harmless 2099 probe" } | ConvertTo-Json -Compress)
if ([string]$approved.data.status -ne "approved" -or -not $approved.data.version_id) { throw "Independent approval did not create an approved version." }

$legacyStatus = Get-HttpStatus {
  Invoke-RestMethod `
    -Uri "$BaseUrl/api/v1/admin/configs" `
    -Method PUT `
    -Headers @{ Authorization = "Bearer $makerToken" } `
    -ContentType "application/json" `
    -Body (@{ key = "acceptance_probe"; value = "must-not-write" } | ConvertTo-Json -Compress)
}
if ($legacyStatus -ne 409) { throw "Legacy single-person config write returned HTTP $legacyStatus instead of 409." }

$unconfigured = Invoke-RestMethod -Uri "$BaseUrl/api/v1/business-variables/membership.middle.monthly_fee" -Method GET
if ([bool]$unconfigured.data.configured) { throw "Acceptance must not configure a real membership price." }

$makerToken = $null
$checkerToken = $null
[ordered]@{
  verdict = "pass"
  environment = "test"
  change_id = $changeID
  probe_key = "club.family.member_capacity"
  probe_value = 20
  probe_effective_at = "2099-01-01T00:00:00Z"
  proposal_status = "pending"
  same_person_review_status = $selfStatus
  independent_review_status = [string]$approved.data.status
  version_created = [bool]$approved.data.version_id
  legacy_direct_write_status = $legacyStatus
  real_membership_price_configured = $false
  credentials_persisted = $false
} | ConvertTo-Json -Depth 4
