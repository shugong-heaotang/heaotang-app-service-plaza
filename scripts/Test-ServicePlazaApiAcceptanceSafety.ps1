$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$acceptancePath = Join-Path $PSScriptRoot "Invoke-ServicePlazaApiAcceptance.ps1"
$otpModulePath = Join-Path $PSScriptRoot "TestAccountOtp.psm1"
$acceptance = Get-Content -LiteralPath $acceptancePath -Raw -Encoding UTF8
$otpModule = Get-Content -LiteralPath $otpModulePath -Raw -Encoding UTF8

$parseErrors = @()
[System.Management.Automation.Language.Parser]::ParseFile($acceptancePath, [ref]$null, [ref]$parseErrors) | Out-Null
[System.Management.Automation.Language.Parser]::ParseFile($otpModulePath, [ref]$null, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -ne 0) {
  throw "API acceptance PowerShell parsing failed: $($parseErrors[0].Message)"
}

$requiredAcceptancePatterns = @(
  'Import-Module (Join-Path $PSScriptRoot "TestAccountOtp.psm1")',
  'Assert-OtpCapacity -TargetPhone $Phone',
  'Assert-OtpCapacity -TargetPhone $IsolationPhone',
  'Get-TestAccountOtpInMemory -Phone $Phone',
  'Get-TestAccountOtpInMemory -Phone $IsolationPhone',
  '$verificationCode = $null',
  '$isolationCode = $null',
  '$token = $null',
  '$isolationToken = $null',
  'secrets_persisted = $false'
)
foreach ($pattern in $requiredAcceptancePatterns) {
  if (-not $acceptance.Contains($pattern)) {
    throw "API acceptance safety invariant is missing: $pattern"
  }
}

if ($acceptance -match 'Payload\.data\.code') {
  throw "API acceptance must not consume a verification code from an HTTP response."
}
if ($acceptance -match 'Write-(Output|Host|Verbose|Debug).*\$(verificationCode|isolationCode|token|isolationToken)') {
  throw "API acceptance must not write OTPs or bearer tokens to output streams."
}

$capacityIndex = $acceptance.IndexOf('Assert-OtpCapacity -TargetPhone $Phone')
$sendCodeIndex = $acceptance.IndexOf('$sendCode = Invoke-JsonRequest')
if ($capacityIndex -lt 0 -or $sendCodeIndex -lt 0 -or $capacityIndex -gt $sendCodeIndex) {
  throw "OTP capacity must be checked before the first send-code request."
}

$requiredOtpPatterns = @(
  'root@47.94.159.60',
  '/root/heaotang-acceptance/runtime/data/heao.db',
  '^1990000999[1-4]$',
  'used = 0',
  "datetime(expires_at) > datetime('now')",
  'ORDER BY id DESC LIMIT 1',
  'RedirectStandardInput = $true',
  'CreateNoWindow = $true'
)
foreach ($pattern in $requiredOtpPatterns) {
  if (-not $otpModule.Contains($pattern)) {
    throw "OTP module safety invariant is missing: $pattern"
  }
}
if ($otpModule -match 'Write-(Output|Host|Verbose|Debug)') {
  throw "OTP module must return only its in-memory function value and must not log secrets."
}

[ordered]@{
  status = "passed"
  environment = "static-only"
  otp_requests_sent = 0
  server_mutations = 0
  http_code_exposure_consumed = $false
  secrets_persisted = $false
} | ConvertTo-Json -Compress
