param(
  [Parameter(Mandatory = $true)][string]$RecordId,
  [Parameter(Mandatory = $true)][string]$Actor,
  [Parameter(Mandatory = $true)][string]$ChecklistPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [int]$AttemptNumber = 1,
  [string]$PreviousAttemptPath = ""
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet
$root = Split-Path $PSScriptRoot -Parent
$bankPath = Join-Path $root "contracts\foundation\governance-exam-bank.v1.json"
$readingListPath = Join-Path $root "contracts\foundation\governance-reading-list.v1.json"
$resolvedChecklist = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ChecklistPath)

if (-not (Test-Path -LiteralPath $resolvedChecklist)) { throw "Completed flight checklist not found: $ChecklistPath" }
$checklistBytes = [IO.File]::ReadAllBytes($resolvedChecklist)
if ($checklistBytes.Length -ge 3 -and $checklistBytes[0] -eq 0xEF -and $checklistBytes[1] -eq 0xBB -and $checklistBytes[2] -eq 0xBF) {
  throw "Completed flight checklist must be canonical UTF-8 without BOM before the exam."
}
$strictUtf8 = New-Object Text.UTF8Encoding($false, $true)
try {
  $checklistText = $strictUtf8.GetString($checklistBytes)
} catch {
  throw "Completed flight checklist must be valid UTF-8 before the exam."
}
if ($checklistText.Contains("`r") -or -not $checklistText.EndsWith("`n")) {
  throw "Completed flight checklist must use LF line endings and one final newline before the exam."
}
$checklist = Get-Content -LiteralPath $resolvedChecklist -Raw -Encoding UTF8 | ConvertFrom-Json
if ($checklist.status -ne "completed" -or $checklist.record_id -ne $RecordId) { throw "Exam requires a completed checklist for the same record_id." }
$readingList = Get-Content -LiteralPath $readingListPath -Raw -Encoding UTF8 | ConvertFrom-Json
$expectedPaths = @($readingList.core)
if ($checklist.module_id) {
  $overlay = $readingList.module_overlays.($checklist.module_id)
  if (-not $overlay) { throw "Checklist references an unknown module overlay: $($checklist.module_id)" }
  $expectedPaths += @($overlay)
}
$expectedPaths = @($expectedPaths | Select-Object -Unique)
$actualPaths = @($checklist.items | ForEach-Object { [string]$_.path })
if (@($expectedPaths | Where-Object { $_ -notin $actualPaths }).Count -gt 0 -or @($actualPaths | Where-Object { $_ -notin $expectedPaths }).Count -gt 0) {
  throw "Checklist does not match the current governance reading list and module overlay."
}
foreach ($item in $checklist.items) {
  $source = Join-Path $root ([string]$item.path)
  if (-not $item.checked -or -not $item.checked_at -or -not (Test-Path -LiteralPath $source)) { throw "Checklist contains an incomplete input: $($item.path)" }
  $currentHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($currentHash -ne [string]$item.sha256) { throw "Checklist input changed and must be reread: $($item.path)" }
}
if ($AttemptNumber -gt 1) {
  if (-not $PreviousAttemptPath) { throw "A retry must reference the previous failed attempt." }
  $previous = Get-Content -LiteralPath $PreviousAttemptPath -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($previous.record_id -ne $RecordId -or $previous.status -ne "failed" -or [int]$previous.attempt_number -ne ($AttemptNumber - 1)) {
    throw "Previous attempt must be the immediately preceding failed exam for this record."
  }
}
$bank = Get-Content -LiteralPath $bankPath -Raw -Encoding UTF8 | ConvertFrom-Json
$selected = @($bank.questions | Get-Random -Count ([int]$bank.question_count_per_attempt))
$suffix = $RecordId -replace '^IR-[0-9]{8}-', ''
$now = [DateTime]::UtcNow.ToString("o")
$attempt = [ordered]@{
  contract_version = "governance-exam.v1"
  attempt_id = "EX-$((Get-Date).ToString('yyyyMMdd'))-$suffix-$AttemptNumber"
  record_id = $RecordId
  actor = $Actor
  attempt_number = $AttemptNumber
  status = "pending"
  generated_at = $now
  completed_at = $null
  question_count = [int]$bank.question_count_per_attempt
  passing_score = [int]$bank.passing_score
  score = $null
  bank_sha256 = (Get-FileHash -LiteralPath $bankPath -Algorithm SHA256).Hash.ToLowerInvariant()
  reading_list_sha256 = (Get-FileHash -LiteralPath $readingListPath -Algorithm SHA256).Hash.ToLowerInvariant()
  checklist_path = $ChecklistPath -replace '\\', '/'
  checklist_sha256 = (Get-FileHash -LiteralPath $resolvedChecklist -Algorithm SHA256).Hash.ToLowerInvariant()
  responses = @($selected | ForEach-Object { [ordered]@{ question_id = $_.question_id; selected_option = $null; correct = $null; source_path = $_.source_path } })
  remediation_sources = @()
}
$target = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputPath)
$directory = Split-Path $target -Parent
if ($directory -and -not (Test-Path -LiteralPath $directory)) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
$json = ($attempt | ConvertTo-Json -Depth 6) -replace "`r?`n", "`n"
[IO.File]::WriteAllText($target, $json.TrimEnd() + "`n", (New-Object Text.UTF8Encoding($false)))

for ($index = 0; $index -lt $selected.Count; $index++) {
  $question = $selected[$index]
  Write-Output "[$($index + 1)] $($question.question_id) $($question.scenario)"
  foreach ($option in $question.options) { Write-Output "  $($option.option_id). $($option.text)" }
}
Write-Output "Submit answers in this displayed order with Submit-AgentGovernanceExam.ps1 -AnswersCsv A,B,C,..."
