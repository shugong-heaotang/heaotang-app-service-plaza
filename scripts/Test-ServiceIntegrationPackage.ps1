param(
  [Parameter(Mandatory = $true)]
  [string[]]$ManifestPath,
  [string]$ActionsPath = "",
  [switch]$CompleteCatalog
)

$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$repoRoot = Split-Path $PSScriptRoot -Parent
$manifestSchema = Join-Path $repoRoot "contracts\service-plaza\service-manifest.schema.json"
$actionSchema = Join-Path $repoRoot "contracts\service-plaza\service-plaza-action.schema.json"
$validator = Join-Path $PSScriptRoot "validate_service_integration_package.py"

$arguments = @(
  "-X", "utf8", $validator,
  "--manifest-schema", $manifestSchema
)
foreach ($path in $ManifestPath) {
  $resolved = (Resolve-Path -LiteralPath $path).Path
  $arguments += @("--manifest", $resolved)
}
if ($ActionsPath) {
  $arguments += @("--action-schema", $actionSchema, "--actions", (Resolve-Path -LiteralPath $ActionsPath).Path)
}
if ($CompleteCatalog) {
  $arguments += "--complete-catalog"
}

$previousPythonUtf8 = $env:PYTHONUTF8
$env:PYTHONUTF8 = "1"
try {
  & python @arguments
  if ($LASTEXITCODE -ne 0) {
    throw "Service Plaza integration package validation failed."
  }
} finally {
  $env:PYTHONUTF8 = $previousPythonUtf8
}
