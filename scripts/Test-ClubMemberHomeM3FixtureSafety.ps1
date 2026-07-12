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
  'ValidateSet("Baseline", "PartialError", "CriticalError", "ApplicationPending", "ApplicationRejected", "DissolvedClub")',
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
  'DELETE FROM club_join_applications WHERE club_id IN',
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
  'Local fixture database must be a .db file under the dedicated temporary test directory.',
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

$pendingPlan = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Plan -Scenario ApplicationPending -RunId "club-member-home-m3-20260712-120003-a1b2c3d7") -join "`n" | ConvertFrom-Json
if ($pendingPlan.expected.application_status -ne "pending" -or $pendingPlan.expected.application_count -ne 1 -or $pendingPlan.expected.membership_count -ne 4) {
  throw "ApplicationPending must create one application without creating a current membership."
}
$rejectedPlan = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Plan -Scenario ApplicationRejected -RunId "club-member-home-m3-20260712-120004-a1b2c3d8") -join "`n" | ConvertFrom-Json
if ($rejectedPlan.expected.application_status -ne "rejected" -or $rejectedPlan.expected.application_count -ne 1 -or $rejectedPlan.expected.membership_count -ne 4) {
  throw "ApplicationRejected must create one application without creating a current membership."
}
$dissolvedPlan = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Plan -Scenario DissolvedClub -RunId "club-member-home-m3-20260712-120005-a1b2c3d9") -join "`n" | ConvertFrom-Json
if ($dissolvedPlan.expected.dissolved_club -ne "run-owned-dissolved-club-active" -or $dissolvedPlan.expected.club_count -ne 6 -or $dissolvedPlan.expected.membership_count -ne 5) {
  throw "DissolvedClub must preserve a run-owned club lifecycle status and its explicit current relationship."
}
if (($dissolvedPlan.identities | Where-Object alias -eq "new-member").expected_state -ne "ready-lifecycle") {
  throw "DissolvedClub must identify the lifecycle-specific synthetic identity state."
}

$localRoot = Join-Path ([IO.Path]::GetTempPath()) "heaotang-cmh-m3-fixture-tests"
$localDb = Join-Path $localRoot "fixture-extension.db"
if (Test-Path -LiteralPath $localRoot) { Remove-Item -LiteralPath $localRoot -Recurse -Force }
[void](New-Item -ItemType Directory -Path $localRoot)
try {
  $schema = @'
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, phone TEXT UNIQUE, name TEXT, role INTEGER, city TEXT);
CREATE TABLE clubs (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, name TEXT, type TEXT, category TEXT, status TEXT, owner_id INTEGER, city TEXT, intro TEXT, member_count INTEGER);
CREATE TABLE club_members (id INTEGER PRIMARY KEY AUTOINCREMENT, club_id INTEGER, user_id INTEGER, role TEXT, UNIQUE(club_id,user_id));
CREATE TABLE club_join_applications (id INTEGER PRIMARY KEY AUTOINCREMENT, club_id INTEGER, user_id INTEGER, message TEXT, status TEXT, review_note TEXT, reviewed_by INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP, reviewed_at TEXT, UNIQUE(club_id,user_id,status));
CREATE TABLE family_tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, club_id INTEGER, title TEXT, owner_user_id INTEGER, status TEXT, due_date TEXT, review_note TEXT);
CREATE TABLE activities (id INTEGER PRIMARY KEY AUTOINCREMENT, club_id INTEGER, code TEXT UNIQUE, title TEXT, start_time TEXT, end_time TEXT, status TEXT, created_by INTEGER);
CREATE TABLE activity_registrations (id INTEGER PRIMARY KEY AUTOINCREMENT, activity_id INTEGER, user_id INTEGER, status TEXT);
CREATE TABLE club_announcements (id INTEGER PRIMARY KEY AUTOINCREMENT, club_id INTEGER, user_id INTEGER, content TEXT);
CREATE TABLE notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, content TEXT, is_read INTEGER, category TEXT, ref_type TEXT, ref_id TEXT);
CREATE TABLE club_member_roles (id INTEGER PRIMARY KEY AUTOINCREMENT, club_id INTEGER, user_id INTEGER, role_id INTEGER);
'@
  $env:CMH_LOCAL_DB = $localDb
  $schema | python.exe -X utf8 -c "import os,sqlite3,sys; con=sqlite3.connect(os.environ['CMH_LOCAL_DB']); con.executescript(sys.stdin.read()); con.commit(); con.close()"
  if ($LASTEXITCODE -ne 0) { throw "Local fixture schema initialization failed." }

  $localScenarios = @("ApplicationPending", "ApplicationRejected", "DissolvedClub")
  $localIndex = 0
  foreach ($localScenario in $localScenarios) {
    $localIndex++
    $localRunId = "club-member-home-m3-20260712-13000$localIndex-b1c2d3e$localIndex"
    $apply = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Apply -Scenario $localScenario -RunId $localRunId -LocalDatabasePath $localDb) -join "`n" | ConvertFrom-Json
    if ($apply.operation -ne "apply" -or $apply.scenario -ne $localScenario) { throw "Local Apply failed for $localScenario." }
    $inspect = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Inspect -Scenario $localScenario -RunId $localRunId -LocalDatabasePath $localDb) -join "`n" | ConvertFrom-Json
    if ($inspect.operation -ne "inspect" -or $inspect.counts.clubs -lt 5) { throw "Local Inspect failed for $localScenario." }
    $cleanup = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Cleanup -Scenario $localScenario -RunId $localRunId -LocalDatabasePath $localDb) -join "`n" | ConvertFrom-Json
    if ($cleanup.remaining.clubs -ne 0 -or $cleanup.remaining.applications -ne 0 -or $cleanup.remaining.memberships -ne 0 -or $cleanup.users_deleted -ne 0) { throw "Local Cleanup failed for $localScenario." }
  }
  $restore = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation RestoreVerify -RunId "club-member-home-m3-20260712-130010-b1c2d3ef" -LocalDatabasePath $localDb) -join "`n" | ConvertFrom-Json
  if (-not $restore.database_restore.dump_sha256_match -or -not $restore.database_restore.local_isolated_mode) { throw "Local RestoreVerify failed." }
} finally {
  Remove-Item Env:CMH_LOCAL_DB -ErrorAction SilentlyContinue
  if (Test-Path -LiteralPath $localRoot) { Remove-Item -LiteralPath $localRoot -Recurse -Force }
}
if (($criticalPlan.identities | Where-Object alias -eq "manager").expected_state -ne "error") {
  throw "CriticalError scenario must affect only the manager identity state."
}

[ordered]@{
  status = "passed"
  environment = "static-plan-and-local-isolated-sqlite"
  run_id_pattern = "unique-timestamp-random-suffix"
  operations = @($plan.operations)
  synthetic_identities = @($plan.identities).Count
  fixture_scenarios = @("Baseline", "PartialError", "CriticalError", "ApplicationPending", "ApplicationRejected", "DissolvedClub")
  partial_error = $partialPlan.expected.partial_error
  critical_error = $criticalPlan.expected.critical_error
  application_pending = $pendingPlan.expected.application_status
  application_rejected = $rejectedPlan.expected.application_status
  dissolved_club = $dissolvedPlan.expected.dissolved_club
  unauthorized = $plan.unauthorized_mechanism
  offline = $plan.offline_mechanism
  maintenance = $plan.maintenance
  server_mutations = 0
  local_apply_inspect_cleanup_scenarios = 3
  local_restore_verify = $true
  otp_requests_sent = 0
  secrets_persisted = $false
} | ConvertTo-Json -Depth 6 -Compress
