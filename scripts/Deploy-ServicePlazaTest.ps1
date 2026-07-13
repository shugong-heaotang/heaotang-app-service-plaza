param(
  [string]$Server = "root@47.94.159.60",
  [string]$BackupScript = "C:\Users\shugo\Documents\heaotang-main\scripts\Backup-TestServerState.ps1",
  [string]$BaseUrl = "https://heaotang.cn",
  [switch]$SimulatePostDeployFailure
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

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
$failedRoot = "/var/www/heaotang/app/service-plaza.failed-$timestamp"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$activated = $false

if (-not (Test-Path -LiteralPath $BackupScript)) {
  throw "Required backup script not found: $BackupScript"
}

$readyBefore = Invoke-RestMethod -Uri "$BaseUrl/ready" -Method GET -TimeoutSec 15
if ($readyBefore.status -ne "ready" -or -not $readyBefore.db) {
  throw "Pre-deployment readiness check failed."
}

& (Join-Path $PSScriptRoot "Build-ServicePlazaTestPackage.ps1")
if ($LASTEXITCODE -ne 0) {
  throw "Frontend build/package validation failed."
}

$indexPath = Join-Path $distRoot "index.html"
$indexHtml = Get-Content -LiteralPath $indexPath -Raw -Encoding UTF8
$assetMatch = [regex]::Match($indexHtml, 'assets/index-[^"'']+\.js')
if (-not $assetMatch.Success) {
  throw "Built frontend index does not reference a versioned JavaScript entry asset."
}
$expectedAsset = $assetMatch.Value

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $BackupScript -Server $Server
if ($LASTEXITCODE -ne 0) {
  throw "Pre-deployment backup failed. Deployment stopped."
}

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

  $failureCommand = if ($SimulatePostDeployFailure) { "false" } else { ":" }
  $remoteScript = @"
set -euo pipefail
target='$targetRoot'
staging='$stagingRoot'
rollback='$rollbackRoot'
failed='$failedRoot'
archive='$remoteArchive'
activated=0
rollback_deployment() {
  if [ "`$activated" -eq 1 ]; then
    if [ -d "`$target" ]; then mv "`$target" "`$failed"; fi
    if [ -d "`$rollback" ]; then mv "`$rollback" "`$target"; fi
  fi
  rm -rf "`$staging"
  rm -f "`$archive"
}
trap rollback_deployment ERR
mkdir -p "`$staging"
tar -xzf "`$archive" -C "`$staging"
test -f "`$staging/index.html"
test -f "`$staging/services/index.html"
test -f "`$staging/$expectedAsset"
if [ -d "`$target" ]; then mv "`$target" "`$rollback"; fi
mv "`$staging" "`$target"
activated=1
chown -R root:root "`$target"
find "`$target" -type d -exec chmod 755 {} +
find "`$target" -type f -exec chmod 644 {} +
grep -Fq '$expectedAsset' "`$target/index.html"
$failureCommand
rm -f "`$archive"
trap - ERR
"@

  $remoteInput = [System.IO.Path]::GetTempFileName()
  $remoteOutput = [System.IO.Path]::GetTempFileName()
  $remoteError = [System.IO.Path]::GetTempFileName()
  try {
    [System.IO.File]::WriteAllText($remoteInput, ($remoteScript -replace "`r", "") + "`n", $utf8NoBom)
    $sshProcess = Start-Process -FilePath "ssh.exe" `
      -ArgumentList @("-o", "BatchMode=yes", $Server, "bash", "-s") `
      -WindowStyle Hidden `
      -RedirectStandardInput $remoteInput `
      -RedirectStandardOutput $remoteOutput `
      -RedirectStandardError $remoteError `
      -Wait `
      -PassThru
    if ($sshProcess.ExitCode -ne 0) {
      $errorText = [System.IO.File]::ReadAllText($remoteError, $utf8NoBom).Trim()
      throw "Remote frontend activation failed and rollback was attempted: $errorText"
    }
    $activated = $true
  } finally {
    Remove-Item -LiteralPath $remoteInput, $remoteOutput, $remoteError -Force -ErrorAction SilentlyContinue
  }

  $verificationPaths = @(
    "/app/service-plaza/services/",
    "/app/service-plaza/services/life-navigation/",
    "/app/service-plaza/services/club-alliance/",
    "/app/service-plaza/services/health-manager/",
    "/app/service-plaza/internal/project-brain/",
    "/app/service-plaza/unknown-path/"
  )
  $publicVerified = $false
  $verifiedPaths = @()
  for ($attempt = 1; $attempt -le 15; $attempt++) {
    try {
      $verifiedPaths = @()
      foreach ($path in $verificationPaths) {
        $separator = if ($path.Contains("?")) { "&" } else { "?" }
        $verificationUrl = "{0}{1}{2}deployment={3}" -f $BaseUrl, $path, $separator, $timestamp
        $publicHtml = (Invoke-WebRequest -UseBasicParsing -Uri $verificationUrl -Headers @{ "Cache-Control" = "no-cache" } -TimeoutSec 15).Content
        if (-not $publicHtml.Contains($expectedAsset)) {
          throw "Deep link $path did not reference the expected entry asset $expectedAsset."
        }
        $verifiedPaths += $path
      }
      if ($verifiedPaths.Count -eq $verificationPaths.Count) {
        $publicVerified = $true
        break
      }
    } catch {
      if ($attempt -eq 15) { throw }
    }
    Start-Sleep -Seconds 1
  }
  if (-not $publicVerified) {
    throw "Public frontend did not reference the expected entry asset $expectedAsset."
  }

  $readyAfter = Invoke-RestMethod -Uri "$BaseUrl/ready" -Method GET -TimeoutSec 15
  if ($readyAfter.status -ne "ready" -or -not $readyAfter.db) {
    throw "Post-deployment readiness check failed."
  }

  [ordered]@{
    deployed_at = [DateTime]::UtcNow.ToString("o")
    target = $targetRoot
    rollback = $rollbackRoot
    remote_archive = $remoteArchive
    expected_asset = $expectedAsset
    public_asset_verified = $publicVerified
    verified_paths = $verifiedPaths
    ready_before = $readyBefore.status
    ready_after = $readyAfter.status
    secrets_persisted = $false
  } | ConvertTo-Json -Compress
} catch {
  $originalError = $_
  if ($activated) {
    $rollbackScript = @"
set -euo pipefail
target='$targetRoot'
rollback='$rollbackRoot'
failed='$failedRoot.public'
if [ -d "`$target" ]; then mv "`$target" "`$failed"; fi
test -d "`$rollback"
mv "`$rollback" "`$target"
"@
    $rollbackInput = [System.IO.Path]::GetTempFileName()
    $rollbackOutput = [System.IO.Path]::GetTempFileName()
    $rollbackError = [System.IO.Path]::GetTempFileName()
    try {
      [System.IO.File]::WriteAllText($rollbackInput, ($rollbackScript -replace "`r", "") + "`n", $utf8NoBom)
      $rollbackProcess = Start-Process -FilePath "ssh.exe" `
        -ArgumentList @("-o", "BatchMode=yes", $Server, "bash", "-s") `
        -WindowStyle Hidden `
        -RedirectStandardInput $rollbackInput `
        -RedirectStandardOutput $rollbackOutput `
        -RedirectStandardError $rollbackError `
        -Wait `
        -PassThru
      if ($rollbackProcess.ExitCode -ne 0) {
        $rollbackStderr = [System.IO.File]::ReadAllText($rollbackError, $utf8NoBom).Trim()
        throw "Frontend verification failed and automatic rollback also failed: $rollbackStderr"
      }

      $rollbackReady = Invoke-RestMethod -Uri "$BaseUrl/ready" -Method GET -TimeoutSec 15
      $rollbackPage = Invoke-WebRequest -UseBasicParsing -Uri "$BaseUrl/app/service-plaza/services/?rollback=$timestamp" -Headers @{ "Cache-Control" = "no-cache" } -TimeoutSec 15
      if ($rollbackReady.status -ne "ready" -or -not $rollbackReady.db -or $rollbackPage.StatusCode -ne 200) {
        throw "Frontend automatic rollback completed but verification failed."
      }
    } finally {
      Remove-Item -LiteralPath $rollbackInput, $rollbackOutput, $rollbackError -Force -ErrorAction SilentlyContinue
    }
  }
  throw $originalError
} finally {
  Remove-Item -LiteralPath $localArchive -Force -ErrorAction SilentlyContinue
}
