param(
  [string]$Server = "root@47.94.159.60",
  [string]$BackupScript = "C:\Users\shugo\Documents\heaotang-main\scripts\Backup-TestServerState.ps1"
)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$repoRoot = Split-Path $PSScriptRoot -Parent
$distRoot = Join-Path $repoRoot "app\dist"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$archiveName = "service-plaza-$timestamp.tar.gz"
$localArchive = Join-Path $env:TEMP $archiveName
$remoteArchive = "/root/heaotang-acceptance/$archiveName.upload"
$targetRoot = "/var/www/heaotang/app/service-plaza"
$stagingRoot = "/var/www/heaotang/app/service-plaza.staging-$timestamp"
$rollbackRoot = "/var/www/heaotang/app/service-plaza.rollback-$timestamp"

if (-not (Test-Path -LiteralPath $BackupScript)) {
  throw "Required backup script not found: $BackupScript"
}

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $BackupScript -Server $Server
if ($LASTEXITCODE -ne 0) {
  throw "Pre-deployment backup failed. Deployment stopped."
}

& (Join-Path $PSScriptRoot "Build-ServicePlazaTestPackage.ps1")

try {
  Push-Location $distRoot
  try {
    & tar.exe -czf $localArchive .
    if ($LASTEXITCODE -ne 0) {
      throw "Unable to create frontend archive."
    }
  } finally {
    Pop-Location
  }

  & scp $localArchive "$Server`:$remoteArchive"
  if ($LASTEXITCODE -ne 0) {
    throw "Frontend archive upload failed."
  }

  $remoteCommand = @(
    "set -e",
    "mkdir -p '$stagingRoot'",
    "tar -xzf '$remoteArchive' -C '$stagingRoot'",
    "test -f '$stagingRoot/index.html'",
    "test -f '$stagingRoot/services/index.html'",
    "if [ -d '$targetRoot' ]; then mv '$targetRoot' '$rollbackRoot'; fi",
    "mv '$stagingRoot' '$targetRoot'",
    "chown -R root:root '$targetRoot'",
    "find '$targetRoot' -type d -exec chmod 755 {} +",
    "find '$targetRoot' -type f -exec chmod 644 {} +"
  ) -join "; "

  & ssh -o BatchMode=yes $Server $remoteCommand
  if ($LASTEXITCODE -ne 0) {
    throw "Remote frontend activation failed."
  }
} finally {
  Remove-Item -LiteralPath $localArchive -Force -ErrorAction SilentlyContinue
}

[ordered]@{
  deployed_at = [DateTime]::UtcNow.ToString("o")
  target = $targetRoot
  rollback = $rollbackRoot
  remote_archive = $remoteArchive
} | ConvertTo-Json -Compress
