param()

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'Initialize-PowerShellUtf8.ps1') -Quiet

$pythonCommand = Get-Command python.exe -ErrorAction Stop
$manager = Join-Path $PSScriptRoot 'Manage-NovaPeopleMigrationDrill.ps1'
$contract = Join-Path (Split-Path $PSScriptRoot -Parent) 'contracts/modules/network/migration/nova-introduction-migration.v1.json'
$schema = Join-Path (Split-Path $PSScriptRoot -Parent) 'contracts/modules/network/migration/nova-introduction-migration.v1.schema.json'
$fixture = Join-Path (Split-Path $PSScriptRoot -Parent) 'contracts/modules/network/migration/fixtures/nova-introduction-migration-fixture.v1.json'
$runId = 'nova-m2-safety-20260712'
$root = Join-Path ([IO.Path]::GetTempPath()) ('nova-m2-drill-' + [Guid]::NewGuid().ToString('N'))
$db = Join-Path $root 'nova-people.drill.db'
$backup = "$db.$runId.backup"

New-Item -ItemType Directory -Path $root | Out-Null
try {
  $setup = @'
import json,sqlite3,sys
db,fixture_path=sys.argv[1:3]
fixture=json.load(open(fixture_path,encoding='utf-8'))
con=sqlite3.connect(db)
con.executescript('''
CREATE TABLE nova_migration_environment(environment TEXT NOT NULL,allow_destructive_drill INTEGER NOT NULL);
INSERT INTO nova_migration_environment VALUES('test',1);
CREATE TABLE introductions(id INTEGER PRIMARY KEY,from_user_id INTEGER NOT NULL,to_user_id INTEGER NOT NULL,via_user_id INTEGER,message TEXT,status TEXT,tenant_id TEXT,created_at TEXT NOT NULL);
''')
for row in fixture['legacy_rows']:
 con.execute('INSERT INTO introductions(id,from_user_id,to_user_id,message,status,tenant_id,created_at) VALUES(?,?,?,?,?,?,?)',(row['id'],row['from_user_id'],row['to_user_id'],row['message'],row['status'],row['tenant_id'],row['created_at']))
con.commit();con.close()
'@
  $setup | & $pythonCommand.Source -X utf8 - $db $fixture
  if ($LASTEXITCODE -ne 0) { throw 'Synthetic database setup failed.' }

  $contractTest = @'
import json,sys
from jsonschema import Draft202012Validator
contract=json.load(open(sys.argv[1],encoding='utf-8'));schema=json.load(open(sys.argv[2],encoding='utf-8'))
Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(contract)
assert contract['executable'] is False
assert contract['safety']['double_write_allowed'] is False
assert contract['rollback']['legacy_write_authority_after_restore']=='forbidden'
assert len(contract['legacy_routes'])==3 and all(x['sunset_status']==410 for x in contract['legacy_routes'])
'@
  $contractTest | & $pythonCommand.Source -X utf8 - $contract $schema
  if ($LASTEXITCODE -ne 0) { throw 'Migration contract validation failed.' }

  $beforeHash = (Get-FileHash -LiteralPath $db -Algorithm SHA256).Hash
  $plan = powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase Plan -DatabasePath $db -RunId $runId -BackupPath $backup -ConfirmTestDatabase | ConvertFrom-Json
  $afterPlanHash = (Get-FileHash -LiteralPath $db -Algorithm SHA256).Hash
  if ($plan.mutation_count -ne 0 -or $beforeHash -ne $afterPlanHash) { throw 'Plan mutated the database.' }

  $apply = powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase Apply -DatabasePath $db -RunId $runId -BackupPath $backup -ConfirmTestDatabase | ConvertFrom-Json
  if ($apply.migrated_count -ne 2 -or $apply.quarantine_count -ne 2 -or $apply.legacy_routes_410 -ne 3 -or $apply.write_block_trigger_count -ne 3) { throw 'Apply result did not match the synthetic fixture.' }
  if (-not (Test-Path -LiteralPath $backup)) { throw 'Apply did not create a backup.' }

  $inspect = powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase Inspect -DatabasePath $db -RunId $runId -BackupPath $backup -ConfirmTestDatabase | ConvertFrom-Json
  if ($inspect.migrated_count -ne 2 -or $inspect.quarantine_count -ne 2) { throw 'Inspect did not preserve migration evidence.' }

  $writeProbe = @'
import sqlite3,sys
con=sqlite3.connect(sys.argv[1])
operation=sys.argv[2]
try:
 if operation == 'insert':
  con.execute("INSERT INTO introductions(id,from_user_id,to_user_id,status,tenant_id,created_at) VALUES(999,1,2,'pending','tenant-alpha','2026-07-12T00:00:00Z')")
 elif operation == 'update':
  con.execute("UPDATE introductions SET status='accepted' WHERE id=101")
 elif operation == 'delete':
  con.execute("DELETE FROM introductions WHERE id=101")
 else:
  raise RuntimeError('UNKNOWN_WRITE_PROBE')
 con.commit();raise SystemExit(2)
except sqlite3.DatabaseError as exc:
 assert 'NOVA_LEGACY_WRITE_FORBIDDEN' in str(exc)
finally:con.close()
'@
  foreach ($operation in @('insert', 'update', 'delete')) {
    $writeProbe | & $pythonCommand.Source -X utf8 - $db $operation
    if ($LASTEXITCODE -ne 0) { throw "Legacy $operation blocking probe failed." }
  }

  $cleanup = powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase Cleanup -DatabasePath $db -RunId $runId -BackupPath $backup -ConfirmTestDatabase | ConvertFrom-Json
  if ($cleanup.migrated_count -ne 0 -or $cleanup.quarantine_count -ne 0 -or $cleanup.legacy_writes_reopened) { throw 'Cleanup did not remain run-bound and fail-closed.' }
  foreach ($operation in @('insert', 'update', 'delete')) {
    $writeProbe | & $pythonCommand.Source -X utf8 - $db $operation
    if ($LASTEXITCODE -ne 0) { throw "Cleanup reopened legacy $operation writes." }
  }

  $restore = powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase RestoreVerify -DatabasePath $db -RunId $runId -BackupPath $backup -ConfirmTestDatabase | ConvertFrom-Json
  if (-not $restore.restore_verified -or $restore.legacy_writes_reopened) { throw 'Restore verification did not preserve the write prohibition.' }

  $unmarkedDb = Join-Path $root 'nova-unmarked.drill.db'
  $missingMarkerSetup = @'
import sqlite3,sys
con=sqlite3.connect(sys.argv[1])
con.execute('CREATE TABLE introductions(id INTEGER PRIMARY KEY)')
con.commit();con.close()
'@
  $missingMarkerSetup | & $pythonCommand.Source -X utf8 - $unmarkedDb
  if ($LASTEXITCODE -ne 0) { throw 'Missing-marker fixture setup failed.' }

  $negativeResults = @()
  $previousErrorAction = $ErrorActionPreference
  $ErrorActionPreference = 'SilentlyContinue'
  & powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase Plan -DatabasePath $db -RunId $runId -BackupPath $backup 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) { $negativeResults += 'missing-confirmation-failed' } else { $negativeResults += 'missing-confirmation-rejected' }
  & powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase Plan -DatabasePath 'C:\production\heao.db' -RunId $runId -BackupPath $backup -ConfirmTestDatabase 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) { $negativeResults += 'production-path-failed' } else { $negativeResults += 'production-path-rejected' }
  & powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase Plan -DatabasePath $unmarkedDb -RunId $runId -BackupPath $backup -ConfirmTestDatabase 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) { $negativeResults += 'missing-test-marker-failed' } else { $negativeResults += 'missing-test-marker-rejected' }
  $backupHashBefore = (Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash
  & powershell -NoProfile -ExecutionPolicy Bypass -File $manager -Phase Apply -DatabasePath $db -RunId $runId -BackupPath $backup -ConfirmTestDatabase 2>$null | Out-Null
  $backupHashAfter = (Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash
  if ($LASTEXITCODE -eq 0 -or $backupHashBefore -ne $backupHashAfter) { $negativeResults += 'existing-backup-failed' } else { $negativeResults += 'existing-backup-rejected' }
  $ErrorActionPreference = $previousErrorAction
  if ($negativeResults -contains 'missing-confirmation-failed' -or
      $negativeResults -contains 'production-path-failed' -or
      $negativeResults -contains 'missing-test-marker-failed' -or
      $negativeResults -contains 'existing-backup-failed') { throw 'Safety negative case was accepted.' }

  [ordered]@{
    status = 'PASS'
    run_id = $runId
    plan_zero_mutation = $true
    migrated = 2
    quarantined = 2
    routes_410 = 3
    double_write_rejected = $true
    insert_update_delete_rejected = $true
    cleanup_run_bound = $true
    restore_verified = $true
    legacy_writes_reopened = $false
    negative_cases = $negativeResults
  } | ConvertTo-Json -Compress
}
finally {
  Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
