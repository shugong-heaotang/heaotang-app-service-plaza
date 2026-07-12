param(
  [ValidateSet("Plan", "Apply", "Inspect", "Cleanup", "RestoreVerify")]
  [string]$Operation = "Plan",
  [string]$Server = "root@47.94.159.60",
  [string]$DatabasePath = "/root/heaotang-acceptance/runtime/data/heao.db",
  [string]$Seed = "HEAOTANG-CMH-M3-20260712-V1",
  [ValidateSet("Baseline", "PartialError", "CriticalError")]
  [string]$Scenario = "Baseline",
  [string]$RunId = ("club-member-home-m3-" + (Get-Date -Format "yyyyMMdd-HHmmss") + "-" + ([Guid]::NewGuid().ToString("N").Substring(0, 8)))
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

if ($Server -ne "root@47.94.159.60" -or $DatabasePath -ne "/root/heaotang-acceptance/runtime/data/heao.db") {
  throw "Fixture operations are restricted to the approved test environment."
}
if ($Seed -ne "HEAOTANG-CMH-M3-20260712-V1") {
  throw "Fixture seed is not approved."
}
if ($RunId -notmatch '^club-member-home-m3-\d{8}-\d{6}-[0-9a-f]{8}$') {
  throw "Fixture RunId must be a unique club-member-home-m3 timestamp and random suffix identifier."
}

$fixturePrefix = "CMH-M3-" + $RunId.Substring("club-member-home-m3-".Length)
$identityDefinitions = @(
  [ordered]@{ alias = "new-member"; phone = "19900009991"; phone_mask = "199****9991"; expected_state = "empty"; can_manage = $false },
  [ordered]@{ alias = "family-member"; phone = "19900009992"; phone_mask = "199****9992"; expected_state = "ready"; can_manage = $false },
  [ordered]@{ alias = "multi-club-member"; phone = "19900009993"; phone_mask = "199****9993"; expected_state = "ready"; can_manage = $false },
  [ordered]@{ alias = "manager"; phone = "19900009994"; phone_mask = "199****9994"; expected_state = "ready"; can_manage = $true }
)
if ($Scenario -eq "PartialError") { $identityDefinitions[1].expected_state = "partial-error" }
if ($Scenario -eq "CriticalError") { $identityDefinitions[3].expected_state = "error" }
$clubCodes = @(
  "$fixturePrefix-FAMILY",
  "$fixturePrefix-GENERAL",
  "$fixturePrefix-CHARITY",
  "$fixturePrefix-MANAGER",
  "$fixturePrefix-CRITICAL-HEALTH"
)

function Quote-Sql([string]$Value) {
  return "'" + $Value.Replace("'", "''") + "'"
}

function Invoke-RemoteSql {
  param([Parameter(Mandatory = $true)][string]$Sql)
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
  [void]$process.Start()
  $process.StandardInput.WriteLine(($Sql -replace "`r", ""))
  $process.StandardInput.Close()
  $stdout = $process.StandardOutput.ReadToEnd()
  $stderr = $process.StandardError.ReadToEnd()
  $process.WaitForExit()
  if ($process.ExitCode -ne 0) {
    throw "Remote fixture SQL failed: $($stderr.Trim())"
  }
  return $stdout.Trim()
}

function Invoke-RemoteShell {
  param([Parameter(Mandatory = $true)][string]$Script)
  $startInfo = New-Object System.Diagnostics.ProcessStartInfo
  $startInfo.FileName = "ssh.exe"
  $startInfo.Arguments = "-o BatchMode=yes -o ConnectTimeout=10 $Server bash -s"
  $startInfo.UseShellExecute = $false
  $startInfo.CreateNoWindow = $true
  $startInfo.RedirectStandardInput = $true
  $startInfo.RedirectStandardOutput = $true
  $startInfo.RedirectStandardError = $true
  $process = New-Object System.Diagnostics.Process
  $process.StartInfo = $startInfo
  [void]$process.Start()
  $process.StandardInput.WriteLine(($Script -replace "`r", ""))
  $process.StandardInput.Close()
  $stdout = $process.StandardOutput.ReadToEnd()
  $stderr = $process.StandardError.ReadToEnd()
  $process.WaitForExit()
  if ($process.ExitCode -ne 0) {
    throw "Remote restore verification failed without changing the live database: $($stderr.Trim())"
  }
  return $stdout.Trim()
}

$quotedCodes = ($clubCodes | ForEach-Object { Quote-Sql $_ }) -join ","
$quotedPhones = ($identityDefinitions | ForEach-Object { Quote-Sql $_.phone }) -join ","
$manifest = [ordered]@{
  contract_version = "club-member-home-m3-fixture.v1"
  seed = $Seed
  run_id = $RunId
  scenario = $Scenario
  fixture_prefix = $fixturePrefix
  environment = "test"
  unique_run_id = $true
  operations = @("Plan", "Apply", "Inspect", "Cleanup", "RestoreVerify")
  identities = @($identityDefinitions | ForEach-Object {
      [ordered]@{
        alias = $_.alias
        phone_mask = $_.phone_mask
        expected_state = $_.expected_state
        can_manage = $_.can_manage
      }
    })
  synthetic_only = $true
  real_data = $false
  secrets_persisted = $false
  production_mutations = 0
  unauthorized_mechanism = "natural-expired-session"
  offline_mechanism = "browser-offline"
  maintenance = "unverified"
  runtime_fault_control = $false
}

if ($Operation -eq "Plan") {
  $manifest.operation = "plan"
  $manifest.expected = [ordered]@{
    identity_count = 4
    club_count = 5
    membership_count = $(if ($Scenario -eq "CriticalError") { 5 } else { 4 })
    task_count = $(if ($Scenario -eq "PartialError") { 2 } else { 1 })
    partial_error = $(if ($Scenario -eq "PartialError") { "run-owned-empty-title-family-task-active" } else { "run-owned-empty-title-family-task-inactive" })
    critical_error = $(if ($Scenario -eq "CriticalError") { "run-owned-standard-health-club-active" } else { "run-owned-standard-health-club-inactive" })
  }
  $manifest | ConvertTo-Json -Depth 8
  exit 0
}

if ($Operation -eq "RestoreVerify") {
  $restoreScript = @'
set -eu
backup="/tmp/__RUN__-backup.db"
restored="/tmp/__RUN__-restored.db"
cleanup() { rm -f "$backup" "$restored"; }
trap cleanup EXIT
sqlite3 "__DB__" ".backup '$backup'"
sqlite3 "$restored" ".restore '$backup'"
integrity=$(sqlite3 -batch -noheader "$restored" "PRAGMA integrity_check;")
schema_count=$(sqlite3 -batch -noheader "$restored" "SELECT COUNT(*) FROM sqlite_master WHERE type IN ('table','index','trigger','view');")
backup_dump_hash=$(sqlite3 -batch "$backup" .dump | sha256sum | awk '{print $1}')
restored_dump_hash=$(sqlite3 -batch "$restored" .dump | sha256sum | awk '{print $1}')
printf '%s|%s|%s|%s\n' "$integrity" "$schema_count" "$backup_dump_hash" "$restored_dump_hash"
'@
  $restoreScript = $restoreScript.Replace("__RUN__", $RunId).Replace("__DB__", $DatabasePath)
  $restoreResult = Invoke-RemoteShell -Script $restoreScript
  $parts = $restoreResult -split '\|', 4
  if ($parts.Count -ne 4 -or $parts[0] -ne "ok" -or [int]$parts[1] -le 0 -or $parts[2] -ne $parts[3]) {
    throw "Database backup/restore integrity comparison failed."
  }
  $manifest.operation = "restore-verify"
  $manifest.database_restore = [ordered]@{
    live_database_unchanged = $true
    restored_to_isolated_file = $true
    integrity_check = "ok"
    schema_object_count = [int]$parts[1]
    dump_sha256_match = $true
    temporary_files_removed = $true
  }
  $manifest | ConvertTo-Json -Depth 8
  exit 0
}

function Get-RunCounts {
  $countsSql = @"
SELECT
  (SELECT COUNT(*) FROM clubs WHERE code IN ($quotedCodes)) || '|' ||
  (SELECT COUNT(*) FROM club_members WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes))) || '|' ||
  (SELECT COUNT(*) FROM family_tasks WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes))) || '|' ||
  (SELECT COUNT(*) FROM activities WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes))) || '|' ||
  (SELECT COUNT(*) FROM activity_registrations WHERE activity_id IN (SELECT id FROM activities WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes)))) || '|' ||
  (SELECT COUNT(*) FROM club_announcements WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes))) || '|' ||
  (SELECT COUNT(*) FROM notifications WHERE ref_type='club_member_home_m3_fixture' AND ref_id=$(Quote-Sql $RunId));
"@
  $raw = Invoke-RemoteSql -Sql $countsSql
  $parts = $raw -split '\|', 7
  if ($parts.Count -ne 7) { throw "Unexpected fixture count row." }
  return [ordered]@{
    clubs = [int]$parts[0]
    memberships = [int]$parts[1]
    tasks = [int]$parts[2]
    activities = [int]$parts[3]
    registrations = [int]$parts[4]
    announcements = [int]$parts[5]
    notifications = [int]$parts[6]
  }
}

if ($Operation -eq "Cleanup") {
  $cleanupSql = @"
BEGIN IMMEDIATE;
DELETE FROM activity_registrations
 WHERE activity_id IN (SELECT id FROM activities WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes)));
DELETE FROM activities WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM club_announcements WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM family_tasks WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM club_member_roles WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM club_members WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM notifications WHERE ref_type='club_member_home_m3_fixture' AND ref_id=$(Quote-Sql $RunId);
DELETE FROM clubs WHERE code IN ($quotedCodes);
COMMIT;
"@
  [void](Invoke-RemoteSql -Sql $cleanupSql)
  $remaining = Get-RunCounts
  foreach ($entry in $remaining.GetEnumerator()) {
    if ([int]$entry.Value -ne 0) { throw "Fixture cleanup left run-owned $($entry.Key)." }
  }
  $manifest.operation = "cleanup"
  $manifest.remaining = $remaining
  $manifest.users_deleted = 0
  $manifest | ConvertTo-Json -Depth 8
  exit 0
}

if ($Operation -eq "Apply") {
  $collision = Invoke-RemoteSql -Sql "SELECT COUNT(*) FROM clubs WHERE code IN ($quotedCodes);"
  if ([int]$collision -ne 0) {
    throw "Fixture RunId already exists. Use Inspect or Cleanup; do not reuse an applied RunId."
  }

  $contaminationSql = @"
SELECT
  (SELECT COUNT(*) FROM club_members cm JOIN users u ON u.id=cm.user_id WHERE u.phone IN ($quotedPhones)) || '|' ||
  (SELECT COUNT(*) FROM clubs c JOIN users u ON u.id=c.owner_id WHERE u.phone IN ($quotedPhones)) || '|' ||
  (SELECT COUNT(*) FROM notifications n JOIN users u ON u.id=n.user_id WHERE u.phone IN ($quotedPhones) AND COALESCE(n.is_read,0)=0);
"@
  $contamination = (Invoke-RemoteSql -Sql $contaminationSql) -split '\|', 3
  if ($contamination.Count -ne 3) { throw "Unexpected synthetic account preflight row." }
  if ([int]$contamination[0] -ne 0 -or [int]$contamination[1] -ne 0 -or [int]$contamination[2] -ne 0) {
    throw "Approved synthetic identity pool is not clean; fixture refuses to delete or overwrite unrelated data."
  }

  $partialErrorSql = ""
  if ($Scenario -eq "PartialError") {
    $partialErrorSql = @"
INSERT INTO family_tasks (club_id,title,owner_user_id,status,due_date,review_note) VALUES
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[0])),'',(SELECT id FROM users WHERE phone='19900009992'),'todo',date('now'),$(Quote-Sql $RunId));
"@
  }
  $criticalErrorSql = ""
  if ($Scenario -eq "CriticalError") {
    $criticalErrorSql = @"
INSERT INTO club_members (club_id,user_id,role) VALUES
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[4])),(SELECT id FROM users WHERE phone='19900009994'),'director');
"@
  }

  $applySql = @"
BEGIN IMMEDIATE;
INSERT OR IGNORE INTO users (phone,name,role,city) VALUES
  ('19900009991','M3 synthetic new member',0,'Beijing'),
  ('19900009992','M3 synthetic family member',0,'Shanghai'),
  ('19900009993','M3 synthetic multi club member',0,'Hangzhou'),
  ('19900009994','M3 synthetic manager',0,'Chengdu');

INSERT INTO clubs (code,name,type,category,status,owner_id,city,intro,member_count) VALUES
  ($(Quote-Sql $clubCodes[0]),'M3 synthetic family club','family','family','active',(SELECT id FROM users WHERE phone='19900009994'),'Shanghai',$(Quote-Sql ("synthetic run " + $RunId)),1),
  ($(Quote-Sql $clubCodes[1]),'M3 synthetic self-created club','standard','general','active',(SELECT id FROM users WHERE phone='19900009994'),'Hangzhou',$(Quote-Sql ("synthetic run " + $RunId)),1),
  ($(Quote-Sql $clubCodes[2]),'M3 synthetic public-benefit club','standard','charity','active',(SELECT id FROM users WHERE phone='19900009994'),'Beijing',$(Quote-Sql ("synthetic run " + $RunId)),1),
  ($(Quote-Sql $clubCodes[3]),'M3 synthetic managed club','standard','general','active',(SELECT id FROM users WHERE phone='19900009994'),'Chengdu',$(Quote-Sql ("synthetic run " + $RunId)),1),
  ($(Quote-Sql $clubCodes[4]),'M3 synthetic critical-error club','standard','health','active',(SELECT id FROM users WHERE phone='19900009994'),'Shenzhen',$(Quote-Sql ("synthetic run " + $RunId)),0);

INSERT INTO club_members (club_id,user_id,role) VALUES
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[0])),(SELECT id FROM users WHERE phone='19900009992'),'member'),
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[1])),(SELECT id FROM users WHERE phone='19900009993'),'member'),
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[2])),(SELECT id FROM users WHERE phone='19900009993'),'member'),
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[3])),(SELECT id FROM users WHERE phone='19900009994'),'director');

INSERT INTO family_tasks (club_id,title,owner_user_id,status,due_date,review_note) VALUES
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[0])),'M3 synthetic family task',(SELECT id FROM users WHERE phone='19900009992'),'todo',date('now'),$(Quote-Sql $RunId));
$partialErrorSql
$criticalErrorSql

INSERT INTO activities (club_id,code,title,start_time,end_time,status,created_by) VALUES
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[0])),$(Quote-Sql ($fixturePrefix + '-ACT-FAMILY')),'M3 synthetic family activity',datetime('now','+1 day'),datetime('now','+1 day','+2 hours'),'published',(SELECT id FROM users WHERE phone='19900009994')),
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[1])),$(Quote-Sql ($fixturePrefix + '-ACT-MULTI')),'M3 synthetic multi-club activity',datetime('now','+2 days'),datetime('now','+2 days','+2 hours'),'published',(SELECT id FROM users WHERE phone='19900009994'));

INSERT INTO activity_registrations (activity_id,user_id,status) VALUES
  ((SELECT id FROM activities WHERE code=$(Quote-Sql ($fixturePrefix + '-ACT-FAMILY'))),(SELECT id FROM users WHERE phone='19900009992'),'registered'),
  ((SELECT id FROM activities WHERE code=$(Quote-Sql ($fixturePrefix + '-ACT-MULTI'))),(SELECT id FROM users WHERE phone='19900009993'),'registered');

INSERT INTO club_announcements (club_id,user_id,content) VALUES
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[0])),(SELECT id FROM users WHERE phone='19900009994'),$(Quote-Sql ("M3 synthetic family feed " + $RunId))),
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[1])),(SELECT id FROM users WHERE phone='19900009994'),$(Quote-Sql ("M3 synthetic self-created feed " + $RunId))),
  ((SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[2])),(SELECT id FROM users WHERE phone='19900009994'),$(Quote-Sql ("M3 synthetic public-benefit feed " + $RunId)));

INSERT INTO notifications (user_id,title,content,is_read,category,ref_type,ref_id) VALUES
  ((SELECT id FROM users WHERE phone='19900009992'),'M3 synthetic notice','synthetic-only',0,'system','club_member_home_m3_fixture',$(Quote-Sql $RunId)),
  ((SELECT id FROM users WHERE phone='19900009993'),'M3 synthetic notice','synthetic-only',0,'system','club_member_home_m3_fixture',$(Quote-Sql $RunId)),
  ((SELECT id FROM users WHERE phone='19900009994'),'M3 synthetic notice','synthetic-only',0,'system','club_member_home_m3_fixture',$(Quote-Sql $RunId));
COMMIT;
"@
  [void](Invoke-RemoteSql -Sql $applySql)
}

$counts = Get-RunCounts
$expectedCounts = [ordered]@{
  clubs = 5
  memberships = $(if ($Scenario -eq "CriticalError") { 5 } else { 4 })
  tasks = $(if ($Scenario -eq "PartialError") { 2 } else { 1 })
  activities = 2
  registrations = 2
  announcements = 3
  notifications = 3
}
foreach ($entry in $expectedCounts.GetEnumerator()) {
  if ([int]$counts[$entry.Key] -ne [int]$entry.Value) {
    throw "Fixture inspection mismatch for $($entry.Key): expected $($entry.Value), found $($counts[$entry.Key])."
  }
}

$criticalMembership = Invoke-RemoteSql -Sql "SELECT COUNT(*) FROM club_members WHERE club_id=(SELECT id FROM clubs WHERE code=$(Quote-Sql $clubCodes[4]));"
$expectedCriticalMembership = $(if ($Scenario -eq "CriticalError") { 1 } else { 0 })
if ([int]$criticalMembership -ne $expectedCriticalMembership) {
  throw "Critical-error membership does not match the selected fixture scenario."
}

$manifest.operation = $Operation.ToLowerInvariant()
$manifest.applied = $true
$manifest.counts = $counts
$manifest.partial_error = [ordered]@{
  mechanism = "run-owned-empty-title-family-task"
  active = ($Scenario -eq "PartialError")
  identity = "family-member"
  stable_error_id = "CMH_TASKS_UNAVAILABLE"
}
$manifest.critical_error = [ordered]@{
  mechanism = "run-owned-standard-health-club"
  prepared = $true
  membership_active = ($Scenario -eq "CriticalError")
  identity = "manager"
  stable_error_id = "CMH_CLUB_CLASSIFICATION_INVALID"
}
$manifest | ConvertTo-Json -Depth 8
