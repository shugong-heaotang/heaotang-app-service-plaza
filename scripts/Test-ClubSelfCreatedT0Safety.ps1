$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$fixturePath = Join-Path $PSScriptRoot "Manage-ClubSelfCreatedT0Fixture.ps1"
$acceptancePath = Join-Path $PSScriptRoot "Invoke-ClubSelfCreatedT0Acceptance.ps1"
$parseErrors = @()
[Management.Automation.Language.Parser]::ParseFile($fixturePath, [ref]$null, [ref]$parseErrors) | Out-Null
[Management.Automation.Language.Parser]::ParseFile($acceptancePath, [ref]$null, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -ne 0) { throw "CA-SC T0 PowerShell parse failed: $($parseErrors[0].Message)" }

$fixture = Get-Content -LiteralPath $fixturePath -Raw -Encoding UTF8
$acceptance = Get-Content -LiteralPath $acceptancePath -Raw -Encoding UTF8

$fixtureRequired = @(
  'ValidateSet("Plan", "Apply", "Inspect", "Cleanup", "RestoreVerify")',
  'HEAOTANG-CA-SC-20260712-V1',
  'root@47.94.159.60',
  '/root/heaotang-acceptance/runtime/data/heao.db',
  'BEGIN IMMEDIATE;',
  'DELETE FROM club_join_applications',
  'DELETE FROM api_idempotency_keys',
  'DELETE FROM clubs WHERE code IN',
  'real_data = $false',
  'secrets_persisted = $false'
)
foreach ($pattern in $fixtureRequired) { if (-not $fixture.Contains($pattern)) { throw "Fixture safety invariant missing: $pattern" } }

$acceptanceRequired = @(
  'RequiredRequests 2',
  'Get-TestAccountOtpInMemory',
  '$code = $null',
  '$tokenA = $null',
  '$tokenB = $null',
  '/api/v1/clubs/search?type=standard&category=general',
  '/api/v1/clubs/self-created/',
  '/api/v1/clubs/join-applications/my',
  'IDEMPOTENCY_KEY_REUSED',
  'Cross-user application isolation failed.',
  'secrets_persisted=$false',
  'production_mutations=0',
  'Assert-ExactFields',
  'Assert-NoForbiddenFields',
  'FixtureRunId'
)
foreach ($pattern in $acceptanceRequired) { if (-not $acceptance.Contains($pattern)) { throw "Acceptance safety invariant missing: $pattern" } }

if ($acceptance -match 'Payload\.data\.code') { throw "Acceptance must not consume OTP from HTTP response." }
if ($acceptance -match 'Write-(Output|Host|Verbose|Debug).*\$(code|token|tokenA|tokenB)') { throw "Acceptance must not output credentials." }
if ($fixture -match '(?i)production|/var/lib|/data/prod') { throw "Fixture script contains a production-like target." }
if ($acceptance -match '/api/v1/clubs($|[?"''])|/create-review|/join-applications/[^m]|/members|/payment|/refund|/withdraw|/federation') {
  throw "Acceptance script contains a forbidden business endpoint."
}

$planOutput = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $fixturePath -Operation Plan
if ($LASTEXITCODE -ne 0) { throw "Fixture plan mode failed." }
$plan = $planOutput | ConvertFrom-Json
if ($plan.operation -ne "plan" -or $plan.club_count -ne 10 -or $plan.expected_self_created_active -ne 5 -or $plan.real_data) {
  throw "Fixture plan is not deterministic or safe."
}

[ordered]@{
  status="passed"
  environment="static-and-plan-only"
  fixed_seed=$plan.seed
  synthetic_clubs=$plan.club_count
  expected_self_created_active=$plan.expected_self_created_active
  otp_requests_sent=0
  server_mutations=0
  secrets_persisted=$false
} | ConvertTo-Json -Compress
