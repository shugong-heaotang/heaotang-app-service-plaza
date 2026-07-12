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
$resolvedRoot = [IO.Path]::GetFullPath($root).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)

function Resolve-RepositoryEvidencePath([string]$PathValue, [string]$Label) {
  $resolved = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($PathValue)
  $full = [IO.Path]::GetFullPath($resolved)
  $prefix = $resolvedRoot + [IO.Path]::DirectorySeparatorChar
  if (-not $full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
    throw "$Label must stay inside the repository: $PathValue"
  }
  return $full
}

function Get-RepositoryRelativePath([string]$FullPath) {
  return $FullPath.Substring($resolvedRoot.Length + 1).Replace('\', '/')
}

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
$previousAttemptRelative = $null
$previousAttemptHash = $null
$remediationRereads = @()
if ($AttemptNumber -gt 1) {
  if (-not $PreviousAttemptPath) { throw "A retry must reference the previous failed attempt." }
  $resolvedPrevious = Resolve-RepositoryEvidencePath $PreviousAttemptPath "Previous attempt"
  if (-not (Test-Path -LiteralPath $resolvedPrevious)) { throw "Previous failed attempt not found: $PreviousAttemptPath" }
  $previous = Get-Content -LiteralPath $resolvedPrevious -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($previous.record_id -ne $RecordId -or $previous.status -ne "failed" -or [int]$previous.attempt_number -ne ($AttemptNumber - 1)) {
    throw "Previous attempt must be the immediately preceding failed exam for this record."
  }
  if (-not $previous.completed_at) { throw "Previous failed attempt must have completed_at evidence." }
  $requiredRemediation = @($previous.remediation_sources | Select-Object -Unique)
  if ($requiredRemediation.Count -eq 0) { throw "Previous failed attempt must list remediation_sources." }
  if ($requiredRemediation.Count -ne @($previous.remediation_sources).Count) { throw "Previous remediation_sources must be unique." }
  $normalizedRequiredRemediation = @($requiredRemediation | ForEach-Object { ([string]$_).Replace('\', '/') })
  $previousAttemptRelative = Get-RepositoryRelativePath $resolvedPrevious
  $previousAttemptHash = (Get-FileHash -LiteralPath $resolvedPrevious -Algorithm SHA256).Hash.ToLowerInvariant()
  $confirmedRemediation = @()
  foreach ($sourcePath in $requiredRemediation) {
    $resolvedSource = Resolve-RepositoryEvidencePath (Join-Path $root ([string]$sourcePath)) "Remediation source"
    if (-not (Test-Path -LiteralPath $resolvedSource)) { throw "Remediation source not found: $sourcePath" }
    $sourceText = Get-Content -LiteralPath $resolvedSource -Raw -Encoding UTF8
    $normalizedSourcePath = ([string]$sourcePath).Replace('\', '/')
    $presentationHash = (Get-FileHash -LiteralPath $resolvedSource -Algorithm SHA256).Hash.ToLowerInvariant()
    $presentationNonce = [Guid]::NewGuid().ToString('N')
    $presentedAt = [DateTime]::UtcNow.ToString("o")
    Write-Output "===== REMEDIATION SOURCE BEGIN: $sourcePath sha256=$presentationHash nonce=$presentationNonce ====="
    Write-Output $sourceText
    Write-Output "===== REMEDIATION SOURCE END: $sourcePath ====="
    $challenge = "$normalizedSourcePath|$presentationNonce"
    $confirmation = Read-Host "After reading the full source, type this exact path and nonce to confirm: $challenge"
    if ($confirmation -cne $challenge) {
      throw "Full remediation source was presented, but its path and nonce were not explicitly confirmed after presentation: $sourcePath"
    }
    if ($normalizedSourcePath -in $confirmedRemediation) {
      throw "A remediation source cannot be confirmed more than once: $sourcePath"
    }
    $confirmedAt = [DateTime]::UtcNow.ToString("o")
    $confirmedRemediation += $normalizedSourcePath
    $remediationRereads += [ordered]@{
      source_path = $normalizedSourcePath
      presented_at = $presentedAt
      presentation_sha256 = $presentationHash
      presentation_nonce = $presentationNonce
      confirmed_at = $confirmedAt
      source_sha256 = $presentationHash
      confirmed_by = $Actor
      confirmation_method = "interactive-path-nonce-after-full-output"
    }
  }
  if ($confirmedRemediation.Count -ne $requiredRemediation.Count) {
    throw "A retry requires explicit confirmation of every previous remediation source and no additional source."
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
if ($AttemptNumber -gt 1) {
  $attempt["previous_attempt_path"] = $previousAttemptRelative
  $attempt["previous_attempt_sha256"] = $previousAttemptHash
  $attempt["remediation_rereads"] = @($remediationRereads)
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
