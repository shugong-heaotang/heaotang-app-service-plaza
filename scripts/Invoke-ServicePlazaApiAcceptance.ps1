param(
  [string]$BaseUrl = "https://heaotang.cn",
  [string]$Phone = "19900009991",
  [string]$IsolationPhone = "19900009993",
  [int]$ClubId = 1,
  [string]$ReportPath = ""
)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

if ($Phone -notmatch '^1[3-9]\d{9}$') {
  throw "Phone must match the backend mobile-number contract."
}
if ($IsolationPhone -notmatch '^1[3-9]\d{9}$' -or $IsolationPhone -eq $Phone) {
  throw "IsolationPhone must be a different number matching the backend mobile-number contract."
}

$BaseUrl = $BaseUrl.TrimEnd("/")
$runId = "service-plaza-uat-" + (Get-Date -Format "yyyyMMdd-HHmmss")
$headers = @{ "Content-Type" = "application/json" }

function Invoke-JsonRequest {
  param(
    [Parameter(Mandatory = $true)][string]$Method,
    [Parameter(Mandatory = $true)][string]$Path,
    [object]$Body,
    [string]$BearerToken = "",
    [hashtable]$ExtraHeaders = @{}
  )

  $requestHeaders = @{}
  foreach ($key in $headers.Keys) {
    $requestHeaders[$key] = $headers[$key]
  }
  if ($BearerToken) {
    $requestHeaders["Authorization"] = "Bearer $BearerToken"
  }
  foreach ($key in $ExtraHeaders.Keys) {
    $requestHeaders[$key] = $ExtraHeaders[$key]
  }

  $params = @{
    Uri = "$BaseUrl$Path"
    Method = $Method
    Headers = $requestHeaders
    UseBasicParsing = $true
  }
  if ($null -ne $Body) {
    $params["Body"] = $Body | ConvertTo-Json -Compress -Depth 8
  }

  try {
    $response = Invoke-WebRequest @params
    $statusCode = [int]$response.StatusCode
    $content = $response.Content
    $responseHeaders = $response.Headers
  } catch {
    $errorResponse = $_.Exception.Response
    if ($null -eq $errorResponse) {
      throw
    }
    $statusCode = [int]$errorResponse.StatusCode
    $responseHeaders = $errorResponse.Headers
    $content = [string]$_.ErrorDetails.Message
    if (-not $content) {
      $reader = New-Object System.IO.StreamReader($errorResponse.GetResponseStream())
      try {
        $content = $reader.ReadToEnd()
      } finally {
        $reader.Dispose()
      }
    }
  }
  $payload = if ($content) { $content | ConvertFrom-Json } else { [pscustomobject]@{} }
  return [pscustomobject]@{
    StatusCode = $statusCode
    Payload = $payload
    Headers = $responseHeaders
  }
}

function Assert-Status {
  param(
    [Parameter(Mandatory = $true)]$Response,
    [Parameter(Mandatory = $true)][int[]]$Expected,
    [Parameter(Mandatory = $true)][string]$Step
  )
  if ($Expected -notcontains $Response.StatusCode) {
    throw "$Step returned HTTP $($Response.StatusCode); expected $($Expected -join '/')."
  }
}

$ready = Invoke-JsonRequest -Method GET -Path "/ready"
Assert-Status $ready @(200) "Readiness"
if (-not $ready.Payload.db -or $ready.Payload.status -ne "ready") {
  throw "Test server is not ready."
}

$unauthenticatedLife = Invoke-JsonRequest -Method POST -Path "/api/v1/life-nav/records" -Body @{
  dimension_id = "yun"
  title = "未登录请求应被拒绝"
}
Assert-Status $unauthenticatedLife @(401) "Unauthenticated Life Navigation submission"

$requestIdProbe = "$runId-request"
$invalidTokenMe = Invoke-JsonRequest -Method GET -Path "/api/v1/auth/me" -BearerToken "invalid-acceptance-token" -ExtraHeaders @{ "X-Request-ID" = $requestIdProbe }
Assert-Status $invalidTokenMe @(401) "Invalid token"
if ([string]$invalidTokenMe.Headers["X-Request-ID"] -ne $requestIdProbe) {
  throw "The backend did not preserve and return X-Request-ID for an authentication error."
}

$sendCode = Invoke-JsonRequest -Method POST -Path "/api/v1/auth/send-code" -Body @{ phone = $Phone }
Assert-Status $sendCode @(200) "Send code"
$verificationCode = [string]$sendCode.Payload.data.code
if ($verificationCode -notmatch '^\d{6}$') {
  throw "The target does not expose a one-time verification code. This acceptance script is restricted to the configured test environment."
}

$login = Invoke-JsonRequest -Method POST -Path "/api/v1/auth/login" -Body @{
  phone = $Phone
  code = $verificationCode
}
Assert-Status $login @(200) "Login"
$token = [string]$login.Payload.data.token
$userId = [int64]$login.Payload.data.user_id
$verificationCode = $null
if (-not $token -or $userId -le 0) {
  throw "Login response is missing the token or user id."
}

$me = Invoke-JsonRequest -Method GET -Path "/api/v1/auth/me" -BearerToken $token
Assert-Status $me @(200) "Current user"
if ([int64]$me.Payload.data.id -ne $userId) {
  throw "Authenticated user identity does not match the login response."
}
if ($me.Payload.data.PSObject.Properties.Name -notcontains "scopes") {
  throw "Current-user response is missing the authoritative scopes array."
}

$invalidLife = Invoke-JsonRequest -Method POST -Path "/api/v1/life-nav/records" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = "$runId-invalid-life" } -Body @{
  title = "缺少维度的请求"
}
Assert-Status $invalidLife @(400) "Life Navigation validation"

$invalidHealth = Invoke-JsonRequest -Method POST -Path "/api/v1/health/consultations" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = "$runId-invalid-health" } -Body @{
  symptoms = "缺少咨询人姓名"
}
Assert-Status $invalidHealth @(400) "Health consultation validation"

$invalidIdempotency = Invoke-JsonRequest -Method POST -Path "/api/v1/health/consultations" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = ("x" * 256) } -Body @{
  patient_name = "幂等键校验"
  symptoms = "无真实健康信息"
}
Assert-Status $invalidIdempotency @(400) "Invalid idempotency key"
if ($invalidIdempotency.Payload.code -ne "INVALID_IDEMPOTENCY_KEY") {
  throw "Invalid Idempotency-Key did not return INVALID_IDEMPOTENCY_KEY."
}
$missingIdempotency = Invoke-JsonRequest -Method POST -Path "/api/v1/health/consultations" -BearerToken $token -Body @{
  patient_name = "缺少幂等键校验"
  symptoms = "无真实健康信息"
}
Assert-Status $missingIdempotency @(400) "Missing idempotency key"
if ($missingIdempotency.Payload.code -ne "INVALID_IDEMPOTENCY_KEY") {
  throw "Missing Idempotency-Key did not return INVALID_IDEMPOTENCY_KEY."
}

$lifeBody = @{
  dimension_id = "yun"
  record_type = "application"
  title = "服务广场导航申请"
  note = "$runId 自动化验收，无真实个人信息"
}
$lifeKey = "$runId-life"
$life = Invoke-JsonRequest -Method POST -Path "/api/v1/life-nav/records" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = $lifeKey } -Body $lifeBody
Assert-Status $life @(201) "Life Navigation submission"
$lifeId = [int64]$life.Payload.data.id
$lifeReplay = Invoke-JsonRequest -Method POST -Path "/api/v1/life-nav/records" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = $lifeKey } -Body $lifeBody
Assert-Status $lifeReplay @(200) "Life Navigation idempotency replay"
if ([int64]$lifeReplay.Payload.data.id -ne $lifeId -or [string]$lifeReplay.Headers["Idempotency-Replayed"] -ne "true") {
  throw "Life Navigation idempotency replay did not return the original resource and replay header."
}
$lifeConflictBody = @{} + $lifeBody
$lifeConflictBody.note = "$runId 同键异载荷必须拒绝"
$lifeConflict = Invoke-JsonRequest -Method POST -Path "/api/v1/life-nav/records" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = $lifeKey } -Body $lifeConflictBody
Assert-Status $lifeConflict @(409) "Life Navigation idempotency key reuse"
if ($lifeConflict.Payload.code -ne "IDEMPOTENCY_KEY_REUSED") {
  throw "Life Navigation idempotency conflict did not return IDEMPOTENCY_KEY_REUSED."
}

$clubBody = @{
  message = "$runId 自动化验收申请"
}
$clubKey = "$runId-club"
$club = Invoke-JsonRequest -Method POST -Path "/api/v1/clubs/$ClubId/join" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = $clubKey } -Body $clubBody
Assert-Status $club @(200, 201) "Club join application"
$clubApplicationId = [int64]$club.Payload.data.application.id

$duplicateClub = Invoke-JsonRequest -Method POST -Path "/api/v1/clubs/$ClubId/join" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = $clubKey } -Body $clubBody
Assert-Status $duplicateClub @(200) "Idempotent club join application"
$duplicateClubApplicationId = [int64]$duplicateClub.Payload.data.application.id
if ($duplicateClubApplicationId -ne $clubApplicationId -or [string]$duplicateClub.Headers["Idempotency-Replayed"] -ne "true") {
  throw "Repeated club join created a second pending application instead of returning the existing application."
}

$healthBody = @{
  patient_name = "服务广场验收-$runId"
  symptoms = "自动化接口验收，无真实健康信息"
}
$healthKey = "$runId-health"
$health = Invoke-JsonRequest -Method POST -Path "/api/v1/health/consultations" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = $healthKey } -Body $healthBody
Assert-Status $health @(201) "Health consultation"
$healthId = [int64]$health.Payload.data.id
$healthReplay = Invoke-JsonRequest -Method POST -Path "/api/v1/health/consultations" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = $healthKey } -Body $healthBody
Assert-Status $healthReplay @(200) "Health consultation idempotency replay"
if ([int64]$healthReplay.Payload.data.id -ne $healthId -or [string]$healthReplay.Headers["Idempotency-Replayed"] -ne "true") {
  throw "Health consultation idempotency replay did not return the original resource and replay header."
}
$healthConflictBody = @{} + $healthBody
$healthConflictBody.symptoms = "$runId 同键异载荷必须拒绝"
$healthConflict = Invoke-JsonRequest -Method POST -Path "/api/v1/health/consultations" -BearerToken $token -ExtraHeaders @{ "Idempotency-Key" = $healthKey } -Body $healthConflictBody
Assert-Status $healthConflict @(409) "Health consultation idempotency key reuse"
if ($healthConflict.Payload.code -ne "IDEMPOTENCY_KEY_REUSED") {
  throw "Health consultation idempotency conflict did not return IDEMPOTENCY_KEY_REUSED."
}

$ownerConsultations = Invoke-JsonRequest -Method GET -Path "/api/v1/health/consultations?page=1&size=100" -BearerToken $token
Assert-Status $ownerConsultations @(200) "Owner consultation list"
$ownerHealthIds = @($ownerConsultations.Payload.data.items | ForEach-Object { [int64]$_.id })
if ($ownerHealthIds -notcontains $healthId) {
  throw "The consultation owner cannot read the newly created consultation."
}

$isolationCodeResponse = Invoke-JsonRequest -Method POST -Path "/api/v1/auth/send-code" -Body @{ phone = $IsolationPhone }
Assert-Status $isolationCodeResponse @(200) "Isolation user send code"
$isolationCode = [string]$isolationCodeResponse.Payload.data.code
if ($isolationCode -notmatch '^\d{6}$') {
  throw "The isolation test account did not receive a test-only verification code."
}
$isolationLogin = Invoke-JsonRequest -Method POST -Path "/api/v1/auth/login" -Body @{
  phone = $IsolationPhone
  code = $isolationCode
}
Assert-Status $isolationLogin @(200) "Isolation user login"
$isolationToken = [string]$isolationLogin.Payload.data.token
$isolationCode = $null
if (-not $isolationToken) {
  throw "Isolation user login did not return a token."
}
$otherConsultations = Invoke-JsonRequest -Method GET -Path "/api/v1/health/consultations?page=1&size=100" -BearerToken $isolationToken
Assert-Status $otherConsultations @(200) "Cross-user consultation list"
$otherHealthIds = @($otherConsultations.Payload.data.items | ForEach-Object { [int64]$_.id })
if ($otherHealthIds -contains $healthId) {
  throw "Health consultation ownership isolation failed."
}
$isolationToken = $null

$token = $null
$maskedPhone = $Phone.Substring(0, 3) + "****" + $Phone.Substring(7, 4)
$report = [ordered]@{
  run_id = $runId
  executed_at = [DateTime]::UtcNow.ToString("o")
  base_url = $BaseUrl
  phone = $maskedPhone
  user_id = $userId
  checks = [ordered]@{
    ready = $ready.StatusCode
    unauthenticated_write = $unauthenticatedLife.StatusCode
    invalid_token = $invalidTokenMe.StatusCode
    request_id_round_trip = $true
    login = $login.StatusCode
    me = $me.StatusCode
    scopes_contract = $true
    life_validation = $invalidLife.StatusCode
    health_validation = $invalidHealth.StatusCode
    invalid_idempotency_key = $invalidIdempotency.StatusCode
    missing_idempotency_key = $missingIdempotency.StatusCode
    life_navigation = [ordered]@{ status = $life.StatusCode; id = $lifeId; replay_status = $lifeReplay.StatusCode; conflict_status = $lifeConflict.StatusCode }
    club_join = [ordered]@{ status = $club.StatusCode; id = $clubApplicationId; club_id = $ClubId }
    duplicate_club_join = [ordered]@{
      status = $duplicateClub.StatusCode
      same_application = $true
      id = $duplicateClubApplicationId
    }
    health_consultation = [ordered]@{ status = $health.StatusCode; id = $healthId; replay_status = $healthReplay.StatusCode; conflict_status = $healthConflict.StatusCode }
    health_owner_list = [ordered]@{ status = $ownerConsultations.StatusCode; contains_created_record = $true }
    health_cross_user_isolation = [ordered]@{ status = $otherConsultations.StatusCode; leaked_record = $false }
  }
  secrets_persisted = $false
}

$reportJson = $report | ConvertTo-Json -Depth 8
if ($ReportPath) {
  $resolvedReportPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ReportPath)
  $reportDirectory = Split-Path $resolvedReportPath -Parent
  if ($reportDirectory -and -not (Test-Path -LiteralPath $reportDirectory)) {
    New-Item -ItemType Directory -Path $reportDirectory -Force | Out-Null
  }
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($resolvedReportPath, $reportJson + "`n", $utf8NoBom)
}

Write-Output $reportJson
