$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$scriptPath = Join-Path $PSScriptRoot "Deploy-ServicePlazaTest.ps1"
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($scriptPath, [ref]$null, [ref]$errors) | Out-Null
if ($errors) {
  throw "Frontend deployment script does not parse: $($errors.Message -join '; ')"
}

$source = Get-Content -LiteralPath $scriptPath -Raw -Encoding UTF8
$requiredPatterns = @(
  'Backup-TestServerState.ps1',
  'trap rollback_deployment ERR',
  'SimulatePostDeployFailure',
  'test -f "`$staging/$expectedAsset"',
  'public_asset_verified',
  'Cache-Control',
  'Post-deployment readiness check failed',
  'automatic rollback also failed',
  'automatic rollback completed but verification failed',
  'secrets_persisted = $false'
)
foreach ($pattern in $requiredPatterns) {
  if (-not $source.Contains($pattern)) {
    throw "Frontend deployment safety invariant is missing: $pattern"
  }
}

$backupIndex = $source.IndexOf('& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $BackupScript')
$uploadIndex = $source.IndexOf('& scp $localArchive')
if ($backupIndex -lt 0 -or $uploadIndex -lt 0 -or $backupIndex -gt $uploadIndex) {
  throw "Pre-deployment backup must complete before any frontend upload."
}

Write-Output "Frontend deployment safety invariants passed."
