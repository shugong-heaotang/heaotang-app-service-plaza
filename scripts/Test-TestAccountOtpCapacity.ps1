param(
  [Parameter(Mandatory = $true)]
  [ValidatePattern('^1[3-9]\d{9}$')]
  [string]$Phone,

  [ValidateRange(1, 5)]
  [int]$RequiredRequests = 1
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$server = "root@47.94.159.60"
$databasePath = "/root/heaotang-acceptance/runtime/data/heao.db"
$dailyLimit = 5
$maskedPhone = $Phone.Substring(0, 3) + "****" + $Phone.Substring($Phone.Length - 4)
$query = "SELECT COUNT(*) || '|' || date('now') FROM verification_codes WHERE phone = '$Phone' AND date(created_at) = date('now');"

$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = "ssh.exe"
$startInfo.Arguments = "-o BatchMode=yes -o ConnectTimeout=10 $server sqlite3 -batch -noheader $databasePath"
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true
$startInfo.RedirectStandardInput = $true
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $startInfo
$started = $false
try {
  if (-not $process.Start()) {
    throw "Unable to start the read-only test-server capacity query."
  }
  $started = $true
  $process.StandardInput.WriteLine($query)
  $process.StandardInput.Close()
  $standardOutput = $process.StandardOutput.ReadToEnd().Trim()
  $standardError = $process.StandardError.ReadToEnd()
  $process.WaitForExit()

  if ($process.ExitCode -ne 0) {
    throw "Read-only test-server capacity query failed with exit code $($process.ExitCode)."
  }
} finally {
  $query = $null
  $standardError = $null
  if ($started -and -not $process.HasExited) {
    $process.Kill()
  }
  $process.Dispose()
}

if ($standardOutput -notmatch '^(\d+)\|(\d{4}-\d{2}-\d{2})$') {
  throw "Test-server capacity query returned an unexpected shape; no quota decision was made."
}

$used = [int]$Matches[1]
$utcDate = $Matches[2]
$remaining = [Math]::Max(0, $dailyLimit - $used)
$capacityReady = $remaining -ge $RequiredRequests

$result = [ordered]@{
  checked_at = [DateTime]::UtcNow.ToString("o")
  environment = "approved-test-server"
  masked_phone = $maskedPhone
  utc_date = $utcDate
  date_basis = "sqlite-date-now-utc"
  daily_limit = $dailyLimit
  used = $used
  remaining = $remaining
  required_requests = $RequiredRequests
  capacity_ready = $capacityReady
  secrets_read = $false
}

$result | ConvertTo-Json -Compress

if (-not $capacityReady) {
  [Console]::Error.WriteLine("Insufficient test-account OTP capacity for ${maskedPhone}: remaining=$remaining required=$RequiredRequests. Wait for natural UTC-day reset or use an already approved test plan.")
  exit 2
}
