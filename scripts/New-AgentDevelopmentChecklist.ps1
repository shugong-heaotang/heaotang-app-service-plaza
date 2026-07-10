param(
  [Parameter(Mandatory = $true)][string]$RecordId,
  [Parameter(Mandatory = $true)][string]$Task,
  [Parameter(Mandatory = $true)][string]$Actor,
  [ValidateSet("", "life-navigation", "club-alliance", "health-manager")][string]$ModuleId = "",
  [Parameter(Mandatory = $true)][string]$OutputPath
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet
$root = Split-Path $PSScriptRoot -Parent
$readingListPath = Join-Path $root "contracts\foundation\governance-reading-list.v1.json"
$readingList = Get-Content -LiteralPath $readingListPath -Raw -Encoding UTF8 | ConvertFrom-Json
$paths = @($readingList.core)
if ($ModuleId) {
  $overlay = $readingList.module_overlays.$ModuleId
  if (-not $overlay) { throw "Unknown module overlay: $ModuleId" }
  $paths += @($overlay)
}
$items = foreach ($relative in $paths | Select-Object -Unique) {
  $path = Join-Path $root $relative
  if (-not (Test-Path -LiteralPath $path)) { throw "Required governance input is missing: $relative" }
  [ordered]@{
    path = $relative
    sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    checked = $false
    checked_at = $null
  }
}
$checklist = [ordered]@{
  contract_version = "development-checklist.v1"
  checklist_id = "FC-$((Get-Date).ToString('yyyyMMdd'))-$($RecordId -replace '^IR-[0-9]{8}-','')"
  record_id = $RecordId
  task = $Task
  actor = $Actor
  module_id = if ($ModuleId) { $ModuleId } else { $null }
  status = "pending"
  created_at = [DateTime]::UtcNow.ToString("o")
  completed_at = $null
  items = @($items)
  attestation = ""
}
$target = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputPath)
$directory = Split-Path $target -Parent
if ($directory -and -not (Test-Path -LiteralPath $directory)) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
$json = (($checklist | ConvertTo-Json -Depth 6) -replace "`r?`n", "`n").TrimEnd() + "`n"
[IO.File]::WriteAllText($target, $json, (New-Object Text.UTF8Encoding($false)))
Write-Output "Pending checklist created. Read every file, then explicitly set each checked=true with checked_at before completion: $target"
