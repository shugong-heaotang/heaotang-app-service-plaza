param(
  [ValidateSet("Plan", "Apply", "Inspect", "Cleanup")]
  [string]$Operation = "Plan",
  [string]$Server = "root@47.94.159.60",
  [string]$DatabasePath = "/root/heaotang-acceptance/runtime/data/heao.db",
  [string]$Seed = "HEAOTANG-CA-SC-20260712-V1"
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

if ($Server -ne "root@47.94.159.60" -or $DatabasePath -ne "/root/heaotang-acceptance/runtime/data/heao.db") {
  throw "Fixture operations are restricted to the approved test environment."
}
if ($Seed -ne "HEAOTANG-CA-SC-20260712-V1") {
  throw "Fixture seed is not approved."
}

$fixturePrefix = "T0-SC-20260712"
$clubs = @(
  [ordered]@{ code="$fixturePrefix-GEN-01"; name="T0自建同心社"; type="standard"; category="general"; status="active"; city="北京"; intro="固定种子合成数据：社区互助"; member_count=7 },
  [ordered]@{ code="$fixturePrefix-GEN-02"; name="T0自建远航社"; type="standard"; category="general"; status="active"; city="上海"; intro="固定种子合成数据：学习交流"; member_count=11 },
  [ordered]@{ code="$fixturePrefix-GEN-03"; name="T0自建青禾社"; type="standard"; category="general"; status="active"; city="杭州"; intro="固定种子合成数据：健康生活"; member_count=13 },
  [ordered]@{ code="$fixturePrefix-GEN-04"; name="T0自建星火社"; type="standard"; category="general"; status="active"; city="成都"; intro="固定种子合成数据：志趣协作"; member_count=17 },
  [ordered]@{ code="$fixturePrefix-GEN-05"; name="T0自建山海社"; type="standard"; category="general"; status="active"; city="深圳"; intro="固定种子合成数据：城市连接"; member_count=19 },
  [ordered]@{ code="$fixturePrefix-CHA-01"; name="T0公益隔离样本"; type="standard"; category="charity"; status="active"; city="北京"; intro="不得进入自建列表"; member_count=3 },
  [ordered]@{ code="$fixturePrefix-FAM-01"; name="T0家庭隔离样本"; type="family"; category="general"; status="active"; city="上海"; intro="不得进入自建列表"; member_count=4 },
  [ordered]@{ code="$fixturePrefix-DIR-01"; name="T0直营隔离样本"; type="direct"; category="general"; status="active"; city="杭州"; intro="不得进入自建列表"; member_count=5 },
  [ordered]@{ code="$fixturePrefix-HEA-01"; name="T0健康分类隔离样本"; type="standard"; category="health"; status="active"; city="成都"; intro="不得进入自建列表"; member_count=6 },
  [ordered]@{ code="$fixturePrefix-INA-01"; name="T0停用隔离样本"; type="standard"; category="general"; status="pending"; city="深圳"; intro="非 active 不得进入列表"; member_count=0 }
)

function Invoke-RemoteSql {
  param([Parameter(Mandatory=$true)][string]$Sql)
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

function Quote-Sql([string]$Value) {
  return "'" + $Value.Replace("'", "''") + "'"
}

$codes = @($clubs | ForEach-Object { $_.code })
$quotedCodes = ($codes | ForEach-Object { Quote-Sql $_ }) -join ","
$manifest = [ordered]@{
  contract_version = "club-sc-t0-fixture.v1"
  seed = $Seed
  fixture_prefix = $fixturePrefix
  environment = "test"
  club_count = $clubs.Count
  expected_self_created_active = 5
  synthetic_accounts = 2
  codes = $codes
  real_data = $false
  secrets_persisted = $false
}

if ($Operation -eq "Plan") {
  $manifest.operation = "plan"
  $manifest | ConvertTo-Json -Depth 6
  exit 0
}

if ($Operation -eq "Cleanup") {
  $cleanupSql = @"
BEGIN IMMEDIATE;
DELETE FROM club_join_applications WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM club_members WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM clubs WHERE code IN ($quotedCodes);
COMMIT;
"@
  [void](Invoke-RemoteSql -Sql $cleanupSql)
  $remaining = Invoke-RemoteSql -Sql "SELECT COUNT(*) FROM clubs WHERE code IN ($quotedCodes);"
  if ([int]$remaining -ne 0) { throw "Fixture cleanup did not remove all synthetic clubs." }
  $manifest.operation = "cleanup"
  $manifest.remaining_clubs = 0
  $manifest | ConvertTo-Json -Depth 6
  exit 0
}

if ($Operation -eq "Apply") {
  $values = @()
  foreach ($club in $clubs) {
    $values += "($(Quote-Sql $club.code),$(Quote-Sql $club.name),$(Quote-Sql $club.type),$(Quote-Sql $club.category),$(Quote-Sql $club.status),$(Quote-Sql $club.city),$(Quote-Sql $club.intro),$($club.member_count))"
  }
  $insertValues = $values -join ",`n"
  $applySql = @"
BEGIN IMMEDIATE;
INSERT OR IGNORE INTO users (phone,name,role,city) VALUES
  ('19900009991','T0合成用户A',0,'北京'),
  ('19900009993','T0合成用户B',0,'上海');
DELETE FROM club_join_applications WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM club_members WHERE club_id IN (SELECT id FROM clubs WHERE code IN ($quotedCodes));
DELETE FROM clubs WHERE code IN ($quotedCodes);
INSERT INTO clubs (code,name,type,category,status,city,intro,member_count,owner_id)
SELECT v.code,v.name,v.type,v.category,v.status,v.city,v.intro,v.member_count,u.id
FROM (
  SELECT column1 AS code,column2 AS name,column3 AS type,column4 AS category,column5 AS status,column6 AS city,column7 AS intro,column8 AS member_count
  FROM (VALUES
$insertValues
  )
) v
CROSS JOIN (SELECT id FROM users WHERE phone='19900009991' LIMIT 1) u;
COMMIT;
"@
  [void](Invoke-RemoteSql -Sql $applySql)
}

$rows = Invoke-RemoteSql -Sql "SELECT id || '|' || code || '|' || type || '|' || COALESCE(category,'') || '|' || status FROM clubs WHERE code IN ($quotedCodes) ORDER BY code;"
$parsed = @()
if ($rows) {
  foreach ($line in ($rows -split "`n")) {
    $parts = $line.Trim() -split '\|', 5
    if ($parts.Count -ne 5) { throw "Unexpected fixture inspection row." }
    $parsed += [ordered]@{ id=[int64]$parts[0]; code=$parts[1]; type=$parts[2]; category=$parts[3]; status=$parts[4] }
  }
}
if ($parsed.Count -ne $clubs.Count) { throw "Fixture inspection expected $($clubs.Count) clubs but found $($parsed.Count)." }
$selfCreated = @($parsed | Where-Object { $_.type -eq "standard" -and $_.category -eq "general" -and $_.status -eq "active" })
if ($selfCreated.Count -ne 5) { throw "Fixture semantic count is not deterministic." }
$manifest.operation = $Operation.ToLowerInvariant()
$manifest.self_created_ids = @($selfCreated | ForEach-Object { $_.id })
$manifest.non_self_created_ids = @($parsed | Where-Object { $selfCreated.id -notcontains $_.id } | ForEach-Object { $_.id })
$manifest | ConvertTo-Json -Depth 6
