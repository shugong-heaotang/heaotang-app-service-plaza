param(
  [Parameter(Mandatory = $true)][string]$AttemptPath,
  [Parameter(Mandatory = $true)][string]$AnswersCsv
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet
$root = Split-Path $PSScriptRoot -Parent
$bankPath = Join-Path $root "contracts\foundation\governance-exam-bank.v1.json"
$resolvedAttempt = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($AttemptPath)
$attempt = Get-Content -LiteralPath $resolvedAttempt -Raw -Encoding UTF8 | ConvertFrom-Json
if ($attempt.status -ne "pending") { throw "Completed or failed exam attempts are immutable; create a new retry attempt." }
$answers = @($AnswersCsv.Split(',') | ForEach-Object { $_.Trim().ToUpperInvariant() })
if ($answers.Count -ne [int]$attempt.question_count -or @($answers | Where-Object { $_ -notin @('A', 'B', 'C') }).Count -gt 0) {
  throw "Provide exactly $($attempt.question_count) comma-separated answers using A, B or C."
}
$bank = Get-Content -LiteralPath $bankPath -Raw -Encoding UTF8 | ConvertFrom-Json
$byID = @{}
foreach ($question in $bank.questions) { $byID[$question.question_id] = $question }
$correctCount = 0
$remediation = @()
for ($index = 0; $index -lt $attempt.responses.Count; $index++) {
  $response = $attempt.responses[$index]
  $question = $byID[$response.question_id]
  if (-not $question) { throw "Unknown question in attempt: $($response.question_id)" }
  $isCorrect = $answers[$index] -eq $question.correct_option
  $response.selected_option = $answers[$index]
  $response.correct = $isCorrect
  if ($isCorrect) { $correctCount++ } else { $remediation += [string]$question.source_path }
}
$score = [int][Math]::Floor(($correctCount * 100) / [int]$attempt.question_count)
$attempt.score = $score
$attempt.status = if ($score -ge [int]$attempt.passing_score) { "passed" } else { "failed" }
$attempt.completed_at = [DateTime]::UtcNow.ToString("o")
$attempt.remediation_sources = @($remediation | Select-Object -Unique)
$json = ($attempt | ConvertTo-Json -Depth 6) -replace "`r?`n", "`n"
[IO.File]::WriteAllText($resolvedAttempt, $json.TrimEnd() + "`n", (New-Object Text.UTF8Encoding($false)))
if ($attempt.status -ne "passed") {
  Write-Error "Governance exam failed with score $score. Reread: $($attempt.remediation_sources -join ', '). Create a new randomized retry; do not modify this failed attempt."
  exit 2
}
Write-Output "Governance exam passed: score=$score attempt_id=$($attempt.attempt_id)"
