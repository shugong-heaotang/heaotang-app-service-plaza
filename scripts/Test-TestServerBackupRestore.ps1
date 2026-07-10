param(
  [string]$Server = "root@47.94.159.60",
  [string]$ArchivePath = "",
  [string]$ReportPath = ""
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

if (-not $ArchivePath) {
  $latest = Get-ChildItem -LiteralPath "D:\Backup\heaotang-test-server" -Filter "test-server-state.tar.gz" -Recurse -File |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
  if (-not $latest) {
    throw "No test-server backup archive was found."
  }
  $ArchivePath = $latest.FullName
}
$archive = (Resolve-Path -LiteralPath $ArchivePath).Path
$validator = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "verify_test_server_backup.py")).Path
$drillID = [Guid]::NewGuid().ToString("N")
$remoteRoot = "/root/heaotang-restore-drill/$drillID"
$remoteArchive = "$remoteRoot/test-server-state.tar.gz"
$remoteValidator = "$remoteRoot/verify_test_server_backup.py"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

& ssh.exe -o BatchMode=yes $Server "mkdir -p '$remoteRoot'"
if ($LASTEXITCODE -ne 0) {
  throw "Unable to create the isolated Linux restore directory."
}
try {
  & scp.exe $archive "$Server`:$remoteArchive"
  if ($LASTEXITCODE -ne 0) {
    throw "Unable to upload the local backup copy for restore verification."
  }
  & scp.exe $validator "$Server`:$remoteValidator"
  if ($LASTEXITCODE -ne 0) {
    throw "Unable to upload the backup verifier."
  }

  $remoteScript = @"
set -euo pipefail
mkdir -p '$remoteRoot/extracted'
tar -xzf '$remoteArchive' -C '$remoteRoot/extracted'
python3 '$remoteValidator' '$remoteRoot/extracted'
"@
  $inputPath = [System.IO.Path]::GetTempFileName()
  $outputPath = [System.IO.Path]::GetTempFileName()
  $errorPath = [System.IO.Path]::GetTempFileName()
  try {
    [System.IO.File]::WriteAllText($inputPath, ($remoteScript -replace "`r", "") + "`n", $utf8NoBom)
    $process = Start-Process -FilePath "ssh.exe" `
      -ArgumentList @("-o", "BatchMode=yes", $Server, "bash", "-s") `
      -WindowStyle Hidden `
      -RedirectStandardInput $inputPath `
      -RedirectStandardOutput $outputPath `
      -RedirectStandardError $errorPath `
      -Wait `
      -PassThru
    if ($process.ExitCode -ne 0) {
      $errorText = [System.IO.File]::ReadAllText($errorPath, $utf8NoBom).Trim()
      throw "Linux backup restore verification failed: $errorText"
    }
    $verificationJson = [System.IO.File]::ReadAllText($outputPath, $utf8NoBom).Trim()
  } finally {
    Remove-Item -LiteralPath $inputPath, $outputPath, $errorPath -Force -ErrorAction SilentlyContinue
  }
  $verification = $verificationJson | ConvertFrom-Json
  $report = [ordered]@{
    executed_at = [DateTime]::UtcNow.ToString("o")
    server = $Server
    archive = $archive
    isolated_linux_restore = $true
    extraction_succeeded = $true
    sqlite_integrity = $verification.sqlite_integrity
    required_tables = $verification.required_tables
    action_count = $verification.action_count
    binary_bytes = $verification.binary_bytes
    startup_script_bytes = $verification.startup_script_bytes
  }
  $json = $report | ConvertTo-Json -Depth 4
  if ($ReportPath) {
    $target = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ReportPath)
    $directory = Split-Path $target -Parent
    if ($directory -and -not (Test-Path -LiteralPath $directory)) {
      New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($target, $json + "`n", $utf8NoBom)
  }
  Write-Output $json
} finally {
  if ($remoteRoot -notmatch '^/root/heaotang-restore-drill/[a-f0-9]{32}$') {
    throw "Refusing to remove an unsafe remote restore path."
  }
  & ssh.exe -o BatchMode=yes $Server "rm -rf -- '$remoteRoot'"
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Unable to clean the isolated Linux restore directory: $remoteRoot"
  }
}
