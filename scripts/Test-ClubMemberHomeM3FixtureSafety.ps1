$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$fixturePath = Join-Path $PSScriptRoot "Manage-ClubMemberHomeM3Fixture.ps1"
$safetyPath = $MyInvocation.MyCommand.Path

foreach ($path in @($fixturePath, $safetyPath)) {
  if (-not (Test-Path -LiteralPath $path)) { throw "Required fixture file is missing: $path" }
  $bytes = [IO.File]::ReadAllBytes($path)
  if ($bytes.Length -lt 3 -or $bytes[0] -ne 0xEF -or $bytes[1] -ne 0xBB -or $bytes[2] -ne 0xBF) {
    throw "PowerShell fixture files must use UTF-8 BOM: $path"
  }
  $text = [Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3)
  if ($text -match "(?<!`r)`n") { throw "PowerShell fixture files must use CRLF: $path" }
  $tokens = $null
  $parseErrors = $null
  [Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$parseErrors) | Out-Null
  if ($parseErrors.Count -ne 0) { throw "PowerShell parse failed for ${path}: $($parseErrors[0].Message)" }
}

$fixture = Get-Content -LiteralPath $fixturePath -Raw -Encoding UTF8
$requiredPatterns = @(
  'ValidateSet("Plan", "Apply", "Inspect", "Cleanup", "RestoreVerify")',
  'ValidateSet("Baseline", "PartialError", "CriticalError")',
  'HEAOTANG-CMH-M3-20260712-V1',
  '^club-member-home-m3-\d{8}-\d{6}-[0-9a-f]{8}$',
  'root@47.94.159.60',
  '/root/heaotang-acceptance/runtime/data/heao.db',
  'BEGIN IMMEDIATE;',
  'Fixture RunId already exists.',
  'fixture refuses to delete or overwrite unrelated data',
  "'19900009991'",
  "'19900009992'",
  "'19900009993'",
  "'19900009994'",
  "'family','family'",
  "'standard','general'",
  "'standard','charity'",
  "'standard','health'",
  "'director'",
  'CMH_TASKS_UNAVAILABLE',
  'CMH_CLUB_CLASSIFICATION_INVALID',
  "'club_member_home_m3_fixture'",
  'DELETE FROM activity_registrations',
  'DELETE FROM activities WHERE club_id IN',
  'DELETE FROM club_announcements WHERE club_id IN',
  'DELETE FROM family_tasks WHERE club_id IN',
  'DELETE FROM club_member_roles WHERE club_id IN',
  'DELETE FROM club_members WHERE club_id IN',
  'DELETE FROM notifications WHERE ref_type=',
  'DELETE FROM clubs WHERE code IN',
  'users_deleted = 0',
  'live_database_unchanged = $true',
  'restored_to_isolated_file = $true',
  'unauthorized_mechanism = "natural-expired-session"',
  'offline_mechanism = "browser-offline"',
  'maintenance = "unverified"',
  'runtime_fault_control = $false',
  'real_data = $false',
  'secrets_persisted = $false',
  'production_mutations = 0'
)
foreach ($pattern in $requiredPatterns) {
  if (-not $fixture.Contains($pattern)) { throw "Fixture safety invariant missing: $pattern" }
}

$forbiddenPatterns = @(
  '(?im)^\s*DELETE\s+FROM\s+users\b',
  '(?im)^\s*UPDATE\s+users\b',
  '(?i)verification_codes',
  '(?i)TestAccountOtp',
  '(?i)Manage-ClubSelfCreatedT0Fixture',
  '(?i)Invoke-ClubSelfCreatedT0Acceptance',
  '(?i)runtime[-_ ]fault[-_ ]control\s*=\s*\$true',
  '(?i)query[-_ ]switch',
  '(?i)(https?://[^\s]+prod|/var/lib|/data/prod|prod\.db)',
  '(?im)^\s*(DROP|ALTER)\s+(TABLE|DATABASE)\b',
  '(?i)(payment|refund|withdraw|subscription)'
)
foreach ($pattern in $forbiddenPatterns) {
  if ($fixture -match $pattern) { throw "Fixture contains forbidden scope or unsafe mutation: $pattern" }
}

$testRunId = "club-member-home-m3-20260712-120000-a1b2c3d4"
$planRaw = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Plan -RunId $testRunId
if ($LASTEXITCODE -ne 0) { throw "Fixture Plan mode failed." }
$planText = $planRaw -join "`n"
if ($planText -match '1990000999[1-4]') { throw "Plan output exposed a complete synthetic phone number." }
$plan = $planText | ConvertFrom-Json

if ($plan.operation -ne "plan" -or $plan.run_id -ne $testRunId -or -not $plan.unique_run_id) {
  throw "Plan output does not prove the unique RunId contract."
}
if (@($plan.operations).Count -ne 5 -or @($plan.identities).Count -ne 4) {
  throw "Plan output must expose five safe operations and four synthetic identities."
}
$aliases = @($plan.identities | ForEach-Object { $_.alias })
foreach ($alias in @("new-member", "family-member", "multi-club-member", "manager")) {
  if ($aliases -notcontains $alias) { throw "Plan output is missing identity $alias." }
}
if ($plan.expected.club_count -ne 5 -or $plan.expected.membership_count -ne 4) {
  throw "Plan output is not deterministic."
}
if ($plan.expected.partial_error -ne "run-owned-empty-title-family-task-inactive") {
  throw "Baseline must leave the run-owned empty-title family task inactive."
}
if ($plan.expected.critical_error -ne "run-owned-standard-health-club-inactive") {
  throw "Baseline must leave the run-owned standard/health club fault inactive."
}
if ($plan.maintenance -ne "unverified" -or $plan.runtime_fault_control -or $plan.real_data -or $plan.production_mutations -ne 0) {
  throw "Fixture plan expanded beyond the authorized non-production boundary."
}
if ($plan.secrets_persisted) { throw "Fixture plan must not persist secrets." }

$partialPlan = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Plan -Scenario PartialError -RunId "club-member-home-m3-20260712-120001-a1b2c3d5") -join "`n" | ConvertFrom-Json
if ($partialPlan.expected.partial_error -ne "run-owned-empty-title-family-task-active" -or $partialPlan.expected.task_count -ne 2) {
  throw "PartialError scenario is not bound to the run-owned empty-title family task."
}
if (($partialPlan.identities | Where-Object alias -eq "family-member").expected_state -ne "partial-error") {
  throw "PartialError scenario must affect only the family-member identity state."
}

$criticalPlan = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Plan -Scenario CriticalError -RunId "club-member-home-m3-20260712-120002-a1b2c3d6") -join "`n" | ConvertFrom-Json
if ($criticalPlan.expected.critical_error -ne "run-owned-standard-health-club-active" -or $criticalPlan.expected.membership_count -ne 5) {
  throw "CriticalError scenario is not bound to the run-owned standard/health club."
}
if (($criticalPlan.identities | Where-Object alias -eq "manager").expected_state -ne "error") {
  throw "CriticalError scenario must affect only the manager identity state."
}

[ordered]@{
  status = "passed"
  environment = "static-and-plan-only"
  run_id_pattern = "unique-timestamp-random-suffix"
  operations = @($plan.operations)
  synthetic_identities = @($plan.identities).Count
  fixture_scenarios = @("Baseline", "PartialError", "CriticalError")
  partial_error = $partialPlan.expected.partial_error
  critical_error = $criticalPlan.expected.critical_error
  unauthorized = $plan.unauthorized_mechanism
  offline = $plan.offline_mechanism
  maintenance = $plan.maintenance
  server_mutations = 0
  otp_requests_sent = 0
  secrets_persisted = $false
} | ConvertTo-Json -Depth 6 -Compress
