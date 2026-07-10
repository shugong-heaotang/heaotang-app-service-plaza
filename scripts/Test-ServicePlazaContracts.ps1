param()

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$repoRoot = Split-Path $PSScriptRoot -Parent
$schema = Join-Path $repoRoot "contracts\service-plaza\service-plaza-action.schema.json"
$baseline = Join-Path $repoRoot "contracts\service-plaza\service-plaza-actions.v1.json"
$foundationRegistry = Join-Path $repoRoot "contracts\foundation\foundation-capabilities.v1.json"

foreach ($path in @($schema, $baseline)) {
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Service Plaza contract file is missing: $path"
  }
  Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null
}

$previousPythonUtf8 = $env:PYTHONUTF8
$env:PYTHONUTF8 = "1"
try {
  & python -X utf8 (Join-Path $PSScriptRoot "validate_service_plaza_contracts.py") $schema $baseline
  if ($LASTEXITCODE -ne 0) {
    throw "Service Plaza action baseline does not satisfy its JSON Schema."
  }
  & python -X utf8 (Join-Path $PSScriptRoot "validate_foundation_dependencies.py") $foundationRegistry --project-root $repoRoot
  if ($LASTEXITCODE -ne 0) {
    throw "Foundation dependency registry validation failed."
  }
  $moduleDependencyFiles = @(
    (Join-Path $repoRoot "contracts\foundation\module-dependencies\life-navigation.v1.json"),
    (Join-Path $repoRoot "contracts\foundation\module-dependencies\club-alliance.v1.json"),
    (Join-Path $repoRoot "contracts\foundation\module-dependencies\health-manager.v1.json")
  )
  $moduleArguments = @($foundationRegistry, "--project-root", $repoRoot)
  foreach ($moduleFile in $moduleDependencyFiles) {
    $moduleArguments += @("--module", $moduleFile)
  }
  & python -X utf8 (Join-Path $PSScriptRoot "validate_foundation_dependencies.py") @moduleArguments
  if ($LASTEXITCODE -ne 0) {
    throw "Module platform dependency validation failed."
  }
  & python -X utf8 (Join-Path $PSScriptRoot "validate_module_internal_dependencies.py") `
    (Join-Path $repoRoot "contracts\foundation\module-internal-dependencies.v1.schema.json") `
    (Join-Path $repoRoot "contracts\modules\life-navigation\internal-dependencies.v1.json") `
    (Join-Path $repoRoot "contracts\modules\club-alliance\internal-dependencies.v1.json") `
    (Join-Path $repoRoot "contracts\modules\health-manager\internal-dependencies.v1.json") `
    --project-root $repoRoot
  if ($LASTEXITCODE -ne 0) {
    throw "Module internal dependency validation failed."
  }
  & python -X utf8 (Join-Path $PSScriptRoot "validate_recurring_issues.py") `
    (Join-Path $repoRoot "contracts\foundation\recurring-issues.v1.schema.json") `
    (Join-Path $repoRoot "contracts\foundation\recurring-issues.v1.json") `
    --project-root $repoRoot
  if ($LASTEXITCODE -ne 0) {
    throw "Recurring issue two-strike validation failed."
  }
  & python -X utf8 (Join-Path $PSScriptRoot "validate_agent_collaboration.py") `
    (Join-Path $repoRoot "contracts\foundation\agent-collaboration.v1.schema.json") `
    (Join-Path $repoRoot "contracts\foundation\agent-collaboration.v1.json")
  if ($LASTEXITCODE -ne 0) {
    throw "Agent workspace ownership and isolation validation failed."
  }
  & python -X utf8 (Join-Path $PSScriptRoot "validate_development_checklists.py") `
    (Join-Path $repoRoot "contracts\foundation\development-checklist.v1.schema.json") `
    (Join-Path $repoRoot "contracts\foundation\development-checklists") `
    --project-root $repoRoot
  if ($LASTEXITCODE -ne 0) {
    throw "AI development flight checklist validation failed."
  }
  & python -X utf8 (Join-Path $PSScriptRoot "validate_implementation_records.py") `
    (Join-Path $repoRoot "contracts\foundation\implementation-record.v1.schema.json") `
    (Join-Path $repoRoot "contracts\foundation\implementation-records") `
    --project-root $repoRoot
  if ($LASTEXITCODE -ne 0) {
    throw "AI implementation record validation failed."
  }
  & python -X utf8 (Join-Path $PSScriptRoot "validate_engineering_standards.py") `
    --project-root $repoRoot `
    --backend-root "C:\Users\shugo\Documents\heaotang-main\backend-go"
  if ($LASTEXITCODE -ne 0) {
    throw "Engineering toolchain standard validation failed."
  }
} finally {
  $env:PYTHONUTF8 = $previousPythonUtf8
}

Write-Host "Service Plaza contract validation passed."
