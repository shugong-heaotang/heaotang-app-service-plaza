param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('Plan', 'Apply', 'Inspect', 'Cleanup', 'RestoreVerify')]
  [string]$Phase,
  [Parameter(Mandatory = $true)]
  [string]$DatabasePath,
  [Parameter(Mandatory = $true)]
  [ValidatePattern('^nova-m2-[a-z0-9][a-z0-9-]{7,63}$')]
  [string]$RunId,
  [string]$BackupPath,
  [switch]$ConfirmTestDatabase
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'Initialize-PowerShellUtf8.ps1') -Quiet

if (-not $ConfirmTestDatabase) {
  throw 'Explicit -ConfirmTestDatabase is required.'
}

$resolvedDatabase = [IO.Path]::GetFullPath($DatabasePath)
$tempRoot = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
if (-not $resolvedDatabase.StartsWith($tempRoot, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'Migration drill database must be under the system temporary directory.'
}
if (-not $resolvedDatabase.EndsWith('.drill.db', [StringComparison]::OrdinalIgnoreCase)) {
  throw 'Migration drill database name must end with .drill.db.'
}
if ($resolvedDatabase -match '(?i)(production|prod|runtime[\\/]data[\\/]heao\.db)') {
  throw 'Production-like database paths are forbidden.'
}
if (-not (Test-Path -LiteralPath $resolvedDatabase -PathType Leaf)) {
  throw "Migration drill database does not exist: $resolvedDatabase"
}

if (-not $BackupPath) {
  $BackupPath = "$resolvedDatabase.$RunId.backup"
}
$resolvedBackup = [IO.Path]::GetFullPath($BackupPath)
if (-not $resolvedBackup.StartsWith($tempRoot, [StringComparison]::OrdinalIgnoreCase)) {
  throw 'Backup must remain under the system temporary directory.'
}

$pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
  throw 'Approved Python runtime was not found on PATH.'
}

$python = @'
import hashlib
import json
import os
import shutil
import sqlite3
import sys

phase, db_path, run_id, backup_path = sys.argv[1:5]

def marker_ok(con):
    row = con.execute("SELECT environment, allow_destructive_drill FROM nova_migration_environment LIMIT 1").fetchone()
    return row == ("test", 1)

def safety_sql(con, run_id_value):
    con.execute("""CREATE TABLE IF NOT EXISTS nova_legacy_route_controls (
      method TEXT NOT NULL,
      path TEXT NOT NULL,
      status_code INTEGER NOT NULL,
      successor TEXT NOT NULL,
      write_enabled INTEGER NOT NULL CHECK(write_enabled=0),
      updated_by_run TEXT NOT NULL,
      PRIMARY KEY(method, path)
    )""")
    con.execute("CREATE TRIGGER IF NOT EXISTS nova_legacy_introductions_block_insert BEFORE INSERT ON introductions BEGIN SELECT RAISE(ABORT, 'NOVA_LEGACY_WRITE_FORBIDDEN'); END")
    con.execute("CREATE TRIGGER IF NOT EXISTS nova_legacy_introductions_block_update BEFORE UPDATE ON introductions BEGIN SELECT RAISE(ABORT, 'NOVA_LEGACY_WRITE_FORBIDDEN'); END")
    con.execute("CREATE TRIGGER IF NOT EXISTS nova_legacy_introductions_block_delete BEFORE DELETE ON introductions BEGIN SELECT RAISE(ABORT, 'NOVA_LEGACY_WRITE_FORBIDDEN'); END")
    routes = [
      ("POST", "/api/v1/network/introductions", 410, "people.connection_send", 0, run_id_value),
      ("PUT", "/api/v1/network/introductions/{id}", 410, "people.connection_status", 0, run_id_value),
      ("POST", "/api/v1/network/referral", 410, "people.connection_draft", 0, run_id_value),
    ]
    con.executemany("INSERT INTO nova_legacy_route_controls(method,path,status_code,successor,write_enabled,updated_by_run) VALUES(?,?,?,?,?,?) ON CONFLICT(method,path) DO UPDATE SET status_code=excluded.status_code,successor=excluded.successor,write_enabled=0,updated_by_run=excluded.updated_by_run", routes)

def inspect(con, run_id_value):
    def scalar(sql, args=()):
        return con.execute(sql, args).fetchone()[0]
    return {
      "source_count": scalar("SELECT COUNT(*) FROM introductions"),
      "migrated_count": scalar("SELECT COUNT(*) FROM introduction_requests WHERE migration_run_id=?", (run_id_value,)) if table_exists(con, "introduction_requests") else 0,
      "quarantine_count": scalar("SELECT COUNT(*) FROM nova_introduction_quarantine WHERE run_id=?", (run_id_value,)) if table_exists(con, "nova_introduction_quarantine") else 0,
      "legacy_routes_410": scalar("SELECT COUNT(*) FROM nova_legacy_route_controls WHERE status_code=410 AND write_enabled=0") if table_exists(con, "nova_legacy_route_controls") else 0,
      "write_block_trigger_count": scalar("SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'nova_legacy_introductions_block_%'"),
    }

def table_exists(con, name):
    return con.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone()[0] == 1

if phase == "Plan":
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    if not marker_ok(con):
        raise RuntimeError("TEST_DATABASE_MARKER_REQUIRED")
    result = {"phase":"Plan", "run_id":run_id, "mutation_count":0, "source_count":con.execute("SELECT COUNT(*) FROM introductions").fetchone()[0]}
    con.close()
elif phase == "Apply":
    check = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    if not marker_ok(check):
        raise RuntimeError("TEST_DATABASE_MARKER_REQUIRED")
    check.close()
    if os.path.exists(backup_path):
        raise RuntimeError("BACKUP_ALREADY_EXISTS")
    source = sqlite3.connect(db_path)
    backup = sqlite3.connect(backup_path)
    source.backup(backup)
    backup.close()
    source.close()
    con = sqlite3.connect(db_path)
    try:
        con.execute("BEGIN IMMEDIATE")
        con.execute("""CREATE TABLE IF NOT EXISTS introduction_requests (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          legacy_source_id INTEGER UNIQUE,
          migration_run_id TEXT NOT NULL,
          tenant_id TEXT NOT NULL,
          from_member_id INTEGER NOT NULL,
          to_member_id INTEGER NOT NULL,
          reason TEXT NOT NULL DEFAULT '',
          self_intro TEXT NOT NULL DEFAULT '',
          status TEXT NOT NULL,
          created_at TEXT NOT NULL
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS nova_introduction_quarantine (
          run_id TEXT NOT NULL,
          legacy_source_id INTEGER NOT NULL,
          reason TEXT NOT NULL,
          source_hash TEXT NOT NULL,
          PRIMARY KEY(run_id, legacy_source_id)
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS nova_introduction_migration_runs (
          run_id TEXT PRIMARY KEY,
          phase TEXT NOT NULL,
          backup_path_hash TEXT NOT NULL
        )""")
        safety_sql(con, run_id)
        migrated = quarantined = 0
        rows = con.execute("SELECT id,from_user_id,to_user_id,status,tenant_id,created_at FROM introductions ORDER BY id").fetchall()
        for source_id, from_id, to_id, status, tenant_id, created_at in rows:
            digest = hashlib.sha256(json.dumps([source_id,from_id,to_id,status,tenant_id,created_at],separators=(',',':')).encode()).hexdigest()
            reason = None
            if not tenant_id:
                reason = "unknown_tenant"
            elif from_id <= 0 or to_id <= 0 or from_id == to_id:
                reason = "invalid_participant"
            elif status not in {"pending", "accepted", "rejected"}:
                reason = "invalid_status"
            elif con.execute("SELECT COUNT(*) FROM introduction_requests WHERE tenant_id=? AND from_member_id=? AND to_member_id=? AND legacy_source_id<>?", (tenant_id,from_id,to_id,source_id)).fetchone()[0]:
                reason = "duplicate_semantics"
            if reason:
                con.execute("INSERT OR IGNORE INTO nova_introduction_quarantine(run_id,legacy_source_id,reason,source_hash) VALUES(?,?,?,?)", (run_id,source_id,reason,digest))
                quarantined += 1
                continue
            before = con.total_changes
            con.execute("INSERT OR IGNORE INTO introduction_requests(legacy_source_id,migration_run_id,tenant_id,from_member_id,to_member_id,reason,self_intro,status,created_at) VALUES(?,?,?,?,?,'migrated legacy introduction','',?,?)", (source_id,run_id,tenant_id,from_id,to_id,status,created_at))
            if con.total_changes > before:
                migrated += 1
        con.execute("INSERT INTO nova_introduction_migration_runs(run_id,phase,backup_path_hash) VALUES(?,?,?)", (run_id,"Apply",hashlib.sha256(backup_path.encode()).hexdigest()))
        con.commit()
        result = {"phase":"Apply", "run_id":run_id, "migrated":migrated, "quarantined":quarantined, "backup_created":True, **inspect(con,run_id)}
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
elif phase == "Inspect":
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    if not marker_ok(con):
        raise RuntimeError("TEST_DATABASE_MARKER_REQUIRED")
    result = {"phase":"Inspect", "run_id":run_id, **inspect(con,run_id)}
    con.close()
elif phase == "Cleanup":
    con = sqlite3.connect(db_path)
    if not marker_ok(con):
        raise RuntimeError("TEST_DATABASE_MARKER_REQUIRED")
    con.execute("BEGIN IMMEDIATE")
    if table_exists(con,"introduction_requests"):
        con.execute("DELETE FROM introduction_requests WHERE migration_run_id=?", (run_id,))
    if table_exists(con,"nova_introduction_quarantine"):
        con.execute("DELETE FROM nova_introduction_quarantine WHERE run_id=?", (run_id,))
    if table_exists(con,"nova_introduction_migration_runs"):
        con.execute("DELETE FROM nova_introduction_migration_runs WHERE run_id=?", (run_id,))
    safety_sql(con, run_id)
    con.commit()
    result = {"phase":"Cleanup", "run_id":run_id, **inspect(con,run_id), "legacy_writes_reopened":False}
    con.close()
elif phase == "RestoreVerify":
    if not os.path.exists(backup_path):
        raise RuntimeError("BACKUP_REQUIRED")
    restored_path = db_path + ".restoreverify"
    if os.path.exists(restored_path):
        os.remove(restored_path)
    source = sqlite3.connect(backup_path)
    restored = sqlite3.connect(restored_path)
    source.backup(restored)
    source_count = source.execute("SELECT COUNT(*) FROM introductions").fetchone()[0]
    safety_sql(restored, run_id)
    restored.commit()
    restored_count = restored.execute("SELECT COUNT(*) FROM introductions").fetchone()[0]
    trigger_count = restored.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'nova_legacy_introductions_block_%'").fetchone()[0]
    route_count = restored.execute("SELECT COUNT(*) FROM nova_legacy_route_controls WHERE status_code=410 AND write_enabled=0").fetchone()[0]
    integrity = restored.execute("PRAGMA integrity_check").fetchone()[0]
    source.close(); restored.close()
    result = {"phase":"RestoreVerify", "run_id":run_id, "restore_verified":source_count==restored_count and trigger_count==3 and route_count==3 and integrity=="ok", "source_count":source_count, "restored_count":restored_count, "legacy_writes_reopened":False, "restored_copy":restored_path}
else:
    raise RuntimeError("UNKNOWN_PHASE")

print(json.dumps(result, separators=(',',':'), sort_keys=True))
'@

$output = $python | & $pythonCommand.Source -X utf8 - $Phase $resolvedDatabase $RunId $resolvedBackup
if ($LASTEXITCODE -ne 0) {
  throw "Migration drill phase failed: $Phase"
}
$output
