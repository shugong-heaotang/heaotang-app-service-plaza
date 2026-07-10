param()

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$root = Split-Path $PSScriptRoot -Parent
$readingListPath = Join-Path $root "contracts\foundation\governance-reading-list.v1.json"
if (-not (Test-Path -LiteralPath $readingListPath)) {
  throw "Governance reading list is missing: $readingListPath"
}
$readingList = Get-Content -LiteralPath $readingListPath -Raw -Encoding UTF8 | ConvertFrom-Json
$required = @($readingList.core | Select-Object -Unique)
$examRequired = @(
  "contracts\foundation\governance-exam-bank.v1.schema.json",
  "contracts\foundation\governance-exam-bank.v1.json",
  "contracts\foundation\governance-exam.v1.schema.json",
  "scripts\New-AgentGovernanceExam.ps1",
  "scripts\Submit-AgentGovernanceExam.ps1",
  "scripts\validate_governance_exams.py"
)
$required += $examRequired

$missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_)) })
if ($missing.Count -gt 0) {
  throw "AI development governance inputs are missing: $($missing -join ', ')"
}

foreach ($relative in $required | Where-Object { $_.EndsWith('.json') }) {
  Get-Content -LiteralPath (Join-Path $root $relative) -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
}

$fingerprints = foreach ($relative in $required) {
  $path = Join-Path $root $relative
  [ordered]@{ path = $relative; sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
}

[ordered]@{
  status = "ready"
  message = "Create and complete the flight checklist, then pass the randomized governance exam with score 100 before editing business code."
  governance_inputs = $fingerprints
} | ConvertTo-Json -Depth 4
