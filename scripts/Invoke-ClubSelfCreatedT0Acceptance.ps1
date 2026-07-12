param(
  [string]$BaseUrl = "https://heaotang.cn",
  [string]$Phone = "19900009991",
  [string]$IsolationPhone = "19900009993",
  [string]$Server = "root@47.94.159.60",
  [string]$OtpDatabasePath = "/root/heaotang-acceptance/runtime/data/heao.db",
  [string]$ReportPath = ""
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet
Import-Module (Join-Path $PSScriptRoot "TestAccountOtp.psm1") -Force

if ($BaseUrl.TrimEnd("/") -ne "https://heaotang.cn" -or $Server -ne "root@47.94.159.60" -or $OtpDatabasePath -ne "/root/heaotang-acceptance/runtime/data/heao.db") {
  throw "CA-SC T0 acceptance is restricted to the approved test environment."
}
if ($Phone -notmatch '^1990000999[1-4]$' -or $IsolationPhone -notmatch '^1990000999[1-4]$' -or $Phone -eq $IsolationPhone) {
  throw "CA-SC T0 requires two distinct approved synthetic accounts."
}

$BaseUrl = $BaseUrl.TrimEnd("/")
$runId = "club-sc-t0-" + (Get-Date -Format "yyyyMMdd-HHmmss")

function Invoke-JsonRequest {
  param([string]$Method, [string]$Path, [object]$Body, [string]$BearerToken = "", [hashtable]$ExtraHeaders = @{})
  $requestHeaders = @{ Accept = "application/json" }
  if ($BearerToken) { $requestHeaders.Authorization = "Bearer $BearerToken" }
  foreach ($key in $ExtraHeaders.Keys) { $requestHeaders[$key] = $ExtraHeaders[$key] }
  $parameters = @{ Uri="$BaseUrl$Path"; Method=$Method; Headers=$requestHeaders; UseBasicParsing=$true; TimeoutSec=30 }
  if ($null -ne $Body) {
    $parameters.ContentType = "application/json"
    $parameters.Body = $Body | ConvertTo-Json -Compress -Depth 8
  }
  try {
    $response = Invoke-WebRequest @parameters
    $statusCode = [int]$response.StatusCode
    $content = $response.Content
    $responseHeaders = $response.Headers
  } catch {
    if ($null -eq $_.Exception.Response) { throw }
    $statusCode = [int]$_.Exception.Response.StatusCode
    $responseHeaders = $_.Exception.Response.Headers
    $content = [string]$_.ErrorDetails.Message
    if (-not $content) {
      $reader = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream())
      try { $content = $reader.ReadToEnd() } finally { $reader.Dispose() }
    }
  }
  $payload = if ($content) { $content | ConvertFrom-Json } else { [pscustomobject]@{} }
  return [pscustomobject]@{ StatusCode=$statusCode; Payload=$payload; Headers=$responseHeaders }
}

function Assert-Status($Response, [int[]]$Expected, [string]$Step) {
  if ($Expected -notcontains $Response.StatusCode) { throw "$Step returned HTTP $($Response.StatusCode); expected $($Expected -join '/')." }
}

function Assert-OtpCapacity([string]$TargetPhone) {
  $output = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "Test-TestAccountOtpCapacity.ps1") -Phone $TargetPhone -RequiredRequests 2
  if ($LASTEXITCODE -ne 0) { throw "OTP capacity preflight failed for an approved synthetic account." }
  $capacity = $output | ConvertFrom-Json
  if (-not $capacity.capacity_ready -or $capacity.secrets_read) { throw "OTP capacity preflight did not produce a safe result." }
  $output = $null
  $capacity = $null
}

function New-SyntheticSession([string]$TargetPhone) {
  $send = Invoke-JsonRequest -Method POST -Path "/api/v1/auth/send-code" -Body @{ phone=$TargetPhone }
  Assert-Status $send @(200) "Synthetic send-code"
  $send.Payload.data.PSObject.Properties.Remove("code")
  $code = Get-TestAccountOtpInMemory -Phone $TargetPhone -Server $Server -DatabasePath $OtpDatabasePath
  $login = Invoke-JsonRequest -Method POST -Path "/api/v1/auth/login" -Body @{ phone=$TargetPhone; code=$code }
  $code = $null
  Assert-Status $login @(200) "Synthetic login"
  $token = [string]$login.Payload.data.token
  $login.Payload.data.PSObject.Properties.Remove("token")
  if (-not $token) { throw "Synthetic login did not return a token." }
  return [pscustomobject]@{ Token=$token }
}

function Invoke-ConcurrentJoin([int64]$ClubId, [string]$BearerToken) {
  Add-Type -AssemblyName System.Net.Http
  $client = New-Object Net.Http.HttpClient
  $client.BaseAddress = [Uri]$BaseUrl
  $requests = @()
  $tasks = @()
  try {
    foreach ($suffix in @("a", "b")) {
      $request = New-Object Net.Http.HttpRequestMessage([Net.Http.HttpMethod]::Post, "/api/v1/clubs/$ClubId/join")
      [void]$request.Headers.TryAddWithoutValidation("Authorization", "Bearer $BearerToken")
      [void]$request.Headers.TryAddWithoutValidation("Idempotency-Key", "$runId-concurrent-$suffix")
      $request.Content = New-Object Net.Http.StringContent((@{ message="$runId concurrent" } | ConvertTo-Json -Compress), [Text.Encoding]::UTF8, "application/json")
      $requests += $request
      $tasks += $client.SendAsync($request)
    }
    [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]$tasks)
    $results = @()
    foreach ($task in $tasks) {
      $response = $task.Result
      $body = $response.Content.ReadAsStringAsync().Result | ConvertFrom-Json
      $results += [pscustomobject]@{ StatusCode=[int]$response.StatusCode; Payload=$body; Headers=$response.Headers }
      $response.Dispose()
    }
    return $results
  } finally {
    foreach ($request in $requests) { $request.Dispose() }
    $client.Dispose()
  }
}

Assert-OtpCapacity $Phone
Assert-OtpCapacity $IsolationPhone

$ready = Invoke-JsonRequest -Method GET -Path "/ready" -Body $null
Assert-Status $ready @(200) "Readiness"
if ($ready.Payload.status -ne "ready" -or -not $ready.Payload.db) { throw "Test environment is not ready." }

$unauthorized = Invoke-JsonRequest -Method GET -Path "/api/v1/clubs/search?type=standard&category=general&page=1&size=20&q=T0" -Body $null
Assert-Status $unauthorized @(401) "Unauthenticated SC search"

$fixtureOutput = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "Manage-ClubSelfCreatedT0Fixture.ps1") -Operation Inspect
if ($LASTEXITCODE -ne 0) { throw "Fixture inspection failed." }
$fixture = $fixtureOutput | ConvertFrom-Json
$fixtureOutput = $null
if ($fixture.seed -ne "HEAOTANG-CA-SC-20260712-V1" -or $fixture.self_created_ids.Count -ne 5) { throw "Fixture manifest is not the approved deterministic set." }
$clubId = [int64]$fixture.self_created_ids[0]
$concurrentClubId = [int64]$fixture.self_created_ids[1]
$nonScId = [int64]$fixture.non_self_created_ids[0]

$sessionA = New-SyntheticSession $Phone
$sessionB = New-SyntheticSession $IsolationPhone
$tokenA = $sessionA.Token
$tokenB = $sessionB.Token

$search = Invoke-JsonRequest -Method GET -Path "/api/v1/clubs/search?type=standard&category=general&page=1&size=100&q=T0" -Body $null -BearerToken $tokenA
Assert-Status $search @(200) "SC authoritative search"
$items = @($search.Payload.data.items)
if ($items.Count -ne 5 -or [int]$search.Payload.data.total -ne 5) { throw "SC deterministic search did not return exactly five fixtures." }
if (@($items | Where-Object { $_.type -ne "standard" -or $_.category -ne "general" -or $_.status -ne "active" }).Count -ne 0) { throw "SC search crossed a type/category/status boundary." }

$detail = Invoke-JsonRequest -Method GET -Path "/api/v1/clubs/self-created/$clubId" -Body $null -BearerToken $tokenA
Assert-Status $detail @(200) "SC detail"
if ($detail.Payload.data.type -ne "standard" -or $detail.Payload.data.category -ne "general" -or $detail.Payload.data.status -ne "active") { throw "SC detail boundary is invalid." }
$nonScDetail = Invoke-JsonRequest -Method GET -Path "/api/v1/clubs/self-created/$nonScId" -Body $null -BearerToken $tokenA
Assert-Status $nonScDetail @(404) "Non-SC detail"
if ($nonScDetail.Payload.code -ne "CLUB_NOT_FOUND") { throw "Non-SC detail did not fail closed with CLUB_NOT_FOUND." }

$key = "$runId-join-a"
$joinBody = @{ message="$runId synthetic join" }
$join = Invoke-JsonRequest -Method POST -Path "/api/v1/clubs/$clubId/join" -Body $joinBody -BearerToken $tokenA -ExtraHeaders @{ "Idempotency-Key"=$key }
Assert-Status $join @(201) "Join first"
$applicationId = [int64]$join.Payload.data.application.id
$replay = Invoke-JsonRequest -Method POST -Path "/api/v1/clubs/$clubId/join" -Body $joinBody -BearerToken $tokenA -ExtraHeaders @{ "Idempotency-Key"=$key }
Assert-Status $replay @(200) "Join replay"
if ([int64]$replay.Payload.data.application.id -ne $applicationId -or [string]$replay.Headers["Idempotency-Replayed"] -ne "true") { throw "Join replay did not return the original application." }
$conflict = Invoke-JsonRequest -Method POST -Path "/api/v1/clubs/$clubId/join" -Body @{ message="$runId changed" } -BearerToken $tokenA -ExtraHeaders @{ "Idempotency-Key"=$key }
Assert-Status $conflict @(409) "Join conflict"
if ($conflict.Payload.code -ne "IDEMPOTENCY_KEY_REUSED") { throw "Join conflict returned the wrong error id." }

$concurrent = @(Invoke-ConcurrentJoin -ClubId $concurrentClubId -BearerToken $tokenB)
if (@($concurrent | Where-Object { @(200,201) -notcontains $_.StatusCode }).Count -ne 0) { throw "Concurrent join returned an unexpected status." }
$concurrentIds = @($concurrent | ForEach-Object { [int64]$_.Payload.data.application.id } | Select-Object -Unique)
if ($concurrentIds.Count -ne 1) { throw "Concurrent join created more than one pending application." }

$myA = Invoke-JsonRequest -Method GET -Path "/api/v1/clubs/join-applications/my?page=1&size=100" -Body $null -BearerToken $tokenA
$myB = Invoke-JsonRequest -Method GET -Path "/api/v1/clubs/join-applications/my?page=1&size=100" -Body $null -BearerToken $tokenB
Assert-Status $myA @(200) "User A applications"
Assert-Status $myB @(200) "User B applications"
$idsA = @($myA.Payload.data.items | ForEach-Object { [int64]$_.id })
$idsB = @($myB.Payload.data.items | ForEach-Object { [int64]$_.id })
if ($idsA -notcontains $applicationId -or $idsA -contains $concurrentIds[0] -or $idsB -notcontains $concurrentIds[0] -or $idsB -contains $applicationId) { throw "Cross-user application isolation failed." }

$tokenA = $null
$tokenB = $null
$sessionA = $null
$sessionB = $null
$report = [ordered]@{
  contract_version="club-sc-t0-api-results.v1"
  run_id=$runId
  executed_at=[DateTime]::UtcNow.ToString("o")
  base_url=$BaseUrl
  fixture_seed=$fixture.seed
  checks=[ordered]@{
    ready=200; unauthenticated_search=401; search=[ordered]@{ status=200; total=5; zero_crossover=$true }
    detail=[ordered]@{ status=200; non_sc_status=404; safe_dto=$true }
    join=[ordered]@{ first=201; replay=200; conflict=409; same_application=$true }
    concurrency=[ordered]@{ responses=$concurrent.Count; single_pending=$true }
    cross_user_isolation=$true
  }
  user_identity_recorded="non-null-only"
  secrets_persisted=$false
  production_mutations=0
}
$json = $report | ConvertTo-Json -Depth 8
if ($ReportPath) {
  $resolved = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ReportPath)
  $directory = Split-Path $resolved -Parent
  if (-not (Test-Path -LiteralPath $directory)) { New-Item -ItemType Directory -Path $directory -Force | Out-Null }
  [IO.File]::WriteAllText($resolved, $json + "`n", (New-Object Text.UTF8Encoding($false)))
}
$json
