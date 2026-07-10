$ErrorActionPreference = "Stop"

function Assert-ApprovedTestOtpTarget {
  param(
    [Parameter(Mandatory = $true)][string]$Server,
    [Parameter(Mandatory = $true)][string]$DatabasePath,
    [Parameter(Mandatory = $true)][string]$Phone
  )

  if ($Server -ne "root@47.94.159.60") {
    throw "OTP retrieval is restricted to the approved test server."
  }
  if ($DatabasePath -ne "/root/heaotang-acceptance/runtime/data/heao.db") {
    throw "OTP retrieval is restricted to the approved test database."
  }
  if ($Phone -notmatch '^1990000999[1-4]$') {
    throw "OTP retrieval is restricted to the approved synthetic test-account pool."
  }
}

function Get-TestAccountOtpInMemory {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory = $true)][string]$Phone,
    [string]$Server = "root@47.94.159.60",
    [string]$DatabasePath = "/root/heaotang-acceptance/runtime/data/heao.db"
  )

  Assert-ApprovedTestOtpTarget -Server $Server -DatabasePath $DatabasePath -Phone $Phone

  $query = "SELECT code FROM verification_codes WHERE phone = '$Phone' AND used = 0 AND datetime(expires_at) > datetime('now') ORDER BY id DESC LIMIT 1;"
  $startInfo = New-Object System.Diagnostics.ProcessStartInfo
  $startInfo.FileName = "ssh.exe"
  $startInfo.Arguments = "-o BatchMode=yes -o ConnectTimeout=10 $Server sqlite3 -batch -noheader $DatabasePath"
  $startInfo.UseShellExecute = $false
  $startInfo.CreateNoWindow = $true
  $startInfo.RedirectStandardInput = $true
  $startInfo.RedirectStandardOutput = $true
  $startInfo.RedirectStandardError = $true

  $process = New-Object System.Diagnostics.Process
  $process.StartInfo = $startInfo
  $started = $false
  $standardOutput = $null
  $standardError = $null
  try {
    if (-not $process.Start()) {
      throw "Unable to start the approved test-server OTP query."
    }
    $started = $true
    $process.StandardInput.WriteLine($query)
    $process.StandardInput.Close()
    $standardOutput = $process.StandardOutput.ReadToEnd().Trim()
    $standardError = $process.StandardError.ReadToEnd()
    $process.WaitForExit()

    if ($process.ExitCode -ne 0) {
      throw "Approved test-server OTP query failed with exit code $($process.ExitCode)."
    }
    if ($standardOutput -notmatch '^\d{6}$') {
      throw "No single unexpired OTP was available for the approved test account."
    }

    return [string]$standardOutput
  } finally {
    $query = $null
    $standardError = $null
    if ($started -and -not $process.HasExited) {
      $process.Kill()
    }
    $process.Dispose()
    $startInfo = $null
  }
}

Export-ModuleMember -Function Get-TestAccountOtpInMemory
