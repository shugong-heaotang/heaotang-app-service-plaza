param(
  [string]$Server = "root@47.94.159.60",
  [string]$BackendRoot = "C:\Users\shugo\Documents\heaotang-main\backend-go",
  [string]$BackupScript = "C:\Users\shugo\Documents\heaotang-main\scripts\Backup-TestServerState.ps1",
  [string]$BaseUrl = "https://heaotang.cn",
  [switch]$RotateSecrets,
  [switch]$SimulatePostDeployFailure
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

function New-HexSecret([int]$ByteCount) {
  $bytes = New-Object byte[] $ByteCount
  $generator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
  try {
    $generator.GetBytes($bytes)
  } finally {
    $generator.Dispose()
  }
  return -join ($bytes | ForEach-Object { $_.ToString("x2") })
}

if (-not (Test-Path -LiteralPath $BackendRoot)) {
  throw "Backend root not found: $BackendRoot"
}
if (-not (Test-Path -LiteralPath $BackupScript)) {
  throw "Backup script not found: $BackupScript"
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$localBinary = Join-Path $env:TEMP "heaotang-service-plaza-$timestamp"
$localStart = Join-Path $env:TEMP "start-acceptance-$timestamp.sh"
$remoteBinaryUpload = "/root/heaotang-acceptance/server.service-plaza-$timestamp.upload"
$remoteStartUpload = "/root/heaotang-acceptance/start-acceptance.service-plaza-$timestamp.upload"
$testPhone = "19900009992"
$oldToken = ""
$activated = $false
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $BackupScript -Server $Server
if ($LASTEXITCODE -ne 0) {
  throw "Pre-deployment backup failed."
}

try {
  if ($RotateSecrets) {
    $sendCode = Invoke-RestMethod -Uri "$BaseUrl/api/v1/auth/send-code" -Method POST -ContentType "application/json" -Body (@{ phone = $testPhone } | ConvertTo-Json -Compress)
    if ([string]$sendCode.data.code -notmatch '^\d{6}$') {
      throw "Unable to create the pre-rotation test session."
    }
    $login = Invoke-RestMethod -Uri "$BaseUrl/api/v1/auth/login" -Method POST -ContentType "application/json" -Body (@{ phone = $testPhone; code = [string]$sendCode.data.code } | ConvertTo-Json -Compress)
    $oldToken = [string]$login.data.token
    $sendCode = $null
    $login = $null
    if (-not $oldToken) {
      throw "Pre-rotation login did not return a token."
    }
  }

  Push-Location $BackendRoot
  try {
    $previousGoos = $env:GOOS
    $previousGoarch = $env:GOARCH
    $previousCgo = $env:CGO_ENABLED
    $env:GOOS = "linux"
    $env:GOARCH = "amd64"
    $env:CGO_ENABLED = "0"
    & go build -trimpath -o $localBinary .\cmd\server
    if ($LASTEXITCODE -ne 0) {
      throw "Linux backend build failed."
    }
  } finally {
    $env:GOOS = $previousGoos
    $env:GOARCH = $previousGoarch
    $env:CGO_ENABLED = $previousCgo
    Pop-Location
  }

  if ($RotateSecrets) {
    & scp "$Server`:/root/heaotang-acceptance/start-acceptance.sh" $localStart
    if ($LASTEXITCODE -ne 0) {
      throw "Unable to download the current startup script for safe rotation."
    }
    $startText = [System.IO.File]::ReadAllText($localStart)
    foreach ($requiredVariable in @("JWT_SECRET", "AUTH_ADMIN_PASSWORD", "MALL_PAYMENT_CALLBACK_SECRET")) {
      if ($startText -notmatch "(?m)^export $requiredVariable=") {
        throw "Startup script is missing required variable $requiredVariable."
      }
    }
    $startText = [regex]::Replace($startText, '(?m)^export JWT_SECRET=.*$', "export JWT_SECRET=$(New-HexSecret 48)")
    $startText = [regex]::Replace($startText, '(?m)^export AUTH_ADMIN_PASSWORD=.*$', "export AUTH_ADMIN_PASSWORD=$(New-HexSecret 32)")
    $startText = [regex]::Replace($startText, '(?m)^export MALL_PAYMENT_CALLBACK_SECRET=.*$', "export MALL_PAYMENT_CALLBACK_SECRET=$(New-HexSecret 32)")
    $startText = [regex]::Replace($startText, '(?m)^export (ALLOW_DEV_OTP|DEV_OTP_CODE)=.*\r?\n?', '')
    $startText = ([regex]::Replace($startText, "`r?`n", "`n")).TrimEnd() + "`n"
    [System.IO.File]::WriteAllText($localStart, $startText, $utf8NoBom)
    $startText = $null
  }

  & scp $localBinary "$Server`:$remoteBinaryUpload"
  if ($LASTEXITCODE -ne 0) {
    throw "Backend upload failed."
  }
  if ($RotateSecrets) {
    & scp $localStart "$Server`:$remoteStartUpload"
    if ($LASTEXITCODE -ne 0) {
      throw "Rotated startup script upload failed."
    }
  }

  $startSetup = ""
  $startRollback = ""
  $startActivate = ""
  if ($RotateSecrets) {
    $startSetup = @"
start='/root/heaotang-acceptance/start-acceptance.sh'
start_rollback='/root/heaotang-acceptance/start-acceptance.rollback-$timestamp.sh'
cp -a "`$start" "`$start_rollback"
bash -n '$remoteStartUpload'
chmod 700 '$remoteStartUpload'
chown root:root '$remoteStartUpload'
"@
    $startRollback = 'cp -a "$start_rollback" "$start"'
    $startActivate = 'mv ''{0}'' "$start"' -f $remoteStartUpload
  }

  $remoteScript = @"
set -euo pipefail
binary='/root/heaotang-acceptance/server'
binary_rollback='/root/heaotang-acceptance/server.rollback-$timestamp'
cp -a "`$binary" "`$binary_rollback"
$startSetup
chmod 755 '$remoteBinaryUpload'
chown root:root '$remoteBinaryUpload'
rollback() {
  binary_restore="`$binary.restore-$timestamp"
  install -m 0755 "`$binary_rollback" "`$binary_restore"
  chown root:root "`$binary_restore"
  mv -f "`$binary_restore" "`$binary"
  $startRollback
  pm2 restart heaotang-server --update-env >/dev/null 2>&1 || true
}
trap rollback ERR
mv '$remoteBinaryUpload' "`$binary"
$startActivate
pm2 restart heaotang-server --update-env >/dev/null
ready=''
for attempt in `$(seq 1 30); do
  if ready=`$(curl -fsS http://127.0.0.1:8081/ready 2>/dev/null); then
    break
  fi
  sleep 1
done
[ -n "`$ready" ]
echo "`$ready" | grep -q '"db":true'
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
      throw "Remote backend activation failed and rollback was attempted: $errorText"
    }
    $activated = $true
  } finally {
    Remove-Item -LiteralPath $remoteInput, $remoteOutput, $remoteError -Force -ErrorAction SilentlyContinue
  }

  $ready = Invoke-RestMethod -Uri "$BaseUrl/ready" -Method GET
  if (-not $ready.db -or [int]$ready.plugins -lt 24) {
    throw "Post-deployment readiness or plugin count is invalid."
  }
  $catalog = Invoke-RestMethod -Uri "$BaseUrl/api/v1/service-plaza/catalog" -Method GET
  if ($catalog.data.contract_version -ne "service-plaza.v1" -or $catalog.data.items.Count -lt 9) {
    throw "Service Plaza catalog verification failed."
  }
  $actions = Invoke-RestMethod -Uri "$BaseUrl/api/v1/service-plaza/actions" -Method GET
  if ($actions.data.contract_version -ne "service-plaza.action.v1" -or [int]$actions.data.count -ne 20 -or $actions.data.items.Count -ne 20) {
    throw "Service Plaza action contract verification failed."
  }
  $baselinePath = Join-Path (Split-Path $PSScriptRoot -Parent) "contracts\service-plaza\service-plaza-actions.v1.json"
  & python -X utf8 (Join-Path $PSScriptRoot "compare_service_plaza_actions.py") $baselinePath "$BaseUrl/api/v1/service-plaza/actions"
  if ($LASTEXITCODE -ne 0) {
    throw "Deployed action catalog differs from the approved machine baseline."
  }
  if ($SimulatePostDeployFailure) {
    throw "Simulated post-deployment verification failure for rollback drill."
  }

  $oldTokenStatus = $null
  if ($RotateSecrets) {
    try {
      Invoke-WebRequest -Uri "$BaseUrl/api/v1/auth/me" -Headers @{ Authorization = "Bearer $oldToken" } -UseBasicParsing | Out-Null
      $oldTokenStatus = 200
    } catch {
      if ($_.Exception.Response) {
        $oldTokenStatus = [int]$_.Exception.Response.StatusCode
      } else {
        throw
      }
    }
    if ($oldTokenStatus -ne 401) {
      throw "Credential rotation verification failed; the pre-rotation token returned HTTP $oldTokenStatus."
    }
  }

  $binaryHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $localBinary).Hash.ToLowerInvariant()
  [ordered]@{
    deployed_at = [DateTime]::UtcNow.ToString("o")
    contract_version = $catalog.data.contract_version
    catalog_services = $catalog.data.items.Count
    action_contract_version = $actions.data.contract_version
    page_actions = $actions.data.items.Count
    plugins = $ready.plugins
    old_session_status = $oldTokenStatus
    secrets_rotated = [bool]$RotateSecrets
    binary_sha256 = $binaryHash
    secrets_persisted = $false
  } | ConvertTo-Json -Compress
} catch {
  if ($activated) {
    $rollbackScript = @"
set -euo pipefail
binary='/root/heaotang-acceptance/server'
binary_restore="`$binary.restore-$timestamp"
install -m 0755 '/root/heaotang-acceptance/server.rollback-$timestamp' "`$binary_restore"
chown root:root "`$binary_restore"
mv -f "`$binary_restore" "`$binary"
if [ -f '/root/heaotang-acceptance/start-acceptance.rollback-$timestamp.sh' ]; then
  cp -a '/root/heaotang-acceptance/start-acceptance.rollback-$timestamp.sh' '/root/heaotang-acceptance/start-acceptance.sh'
fi
pm2 restart heaotang-server --update-env >/dev/null
for attempt in `$(seq 1 30); do
  curl -fsS http://127.0.0.1:8081/ready >/dev/null 2>&1 && exit 0
  sleep 1
done
exit 1
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
        $rollbackStdout = [System.IO.File]::ReadAllText($rollbackOutput, $utf8NoBom).Trim()
        $rollbackStderr = [System.IO.File]::ReadAllText($rollbackError, $utf8NoBom).Trim()
        throw "Post-deployment verification failed and automatic rollback also failed. Manual recovery is required. stdout=$rollbackStdout stderr=$rollbackStderr"
      }
    } finally {
      Remove-Item -LiteralPath $rollbackInput, $rollbackOutput, $rollbackError -Force -ErrorAction SilentlyContinue
    }
  }
  throw
} finally {
  $oldToken = $null
  Remove-Item -LiteralPath $localBinary, $localStart -Force -ErrorAction SilentlyContinue
}
