param(
  [string]$Server = "root@47.94.159.60",
  [string]$BaseUrl = "https://heaotang.cn",
  [string]$ReportPath = ""
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

function Get-RemoteBinaryHash {
  $value = & ssh.exe -o BatchMode=yes $Server "sha256sum /root/heaotang-acceptance/server | awk '{print `$1}'"
  if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($value)) {
    throw "Unable to read the test-server binary hash."
  }
  return ([string]$value).Trim().ToLowerInvariant()
}

$beforeHash = Get-RemoteBinaryHash
$stdout = [System.IO.Path]::GetTempFileName()
$stderr = [System.IO.Path]::GetTempFileName()
try {
  $process = Start-Process -FilePath "powershell.exe" `
    -ArgumentList @(
      "-NoProfile", "-ExecutionPolicy", "Bypass",
      "-File", (Join-Path $PSScriptRoot "Deploy-ServicePlazaBackendTest.ps1"),
      "-Server", $Server,
      "-BaseUrl", $BaseUrl,
      "-SimulatePostDeployFailure"
    ) `
    -WindowStyle Hidden `
    -RedirectStandardOutput $stdout `
    -RedirectStandardError $stderr `
    -Wait `
    -PassThru
  if ($process.ExitCode -eq 0) {
    throw "Rollback drill did not trigger the expected post-deployment failure."
  }
  $childOutput = [System.IO.File]::ReadAllText($stdout) + "`n" + [System.IO.File]::ReadAllText($stderr)
  if ($childOutput -notmatch "Simulated post-deployment verification failure") {
    throw "The deployment failed before the rollback drill reached its simulated post-deployment gate. Child output: $childOutput"
  }
} finally {
  Remove-Item -LiteralPath $stdout, $stderr -Force -ErrorAction SilentlyContinue
}

$afterHash = Get-RemoteBinaryHash
if ($afterHash -ne $beforeHash) {
  throw "Automatic rollback did not restore the original server binary."
}
$ready = Invoke-RestMethod -Uri "$($BaseUrl.TrimEnd('/'))/ready" -Method GET
if ($ready.status -ne "ready" -or -not $ready.db) {
  throw "The test server is not ready after the rollback drill."
}

$report = [ordered]@{
  executed_at = [DateTime]::UtcNow.ToString("o")
  server = $Server
  expected_failure_observed = $true
  original_binary_restored = $true
  binary_sha256 = $afterHash
  ready = $true
  database_ready = [bool]$ready.db
}
$json = $report | ConvertTo-Json -Depth 4
if ($ReportPath) {
  $target = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ReportPath)
  $directory = Split-Path $target -Parent
  if ($directory -and -not (Test-Path -LiteralPath $directory)) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
  }
  [System.IO.File]::WriteAllText($target, $json + "`n", (New-Object System.Text.UTF8Encoding($false)))
}
Write-Output $json
