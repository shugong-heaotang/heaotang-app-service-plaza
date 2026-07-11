param(
  [Parameter(Mandatory = $true)]
  [string[]]$ManifestPath,
  [string]$ActionsPath = "",
  [switch]$CompleteCatalog,
  [string]$DistRoot = "",
  [string[]]$ExpectedRoute = @()
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

if ($ExpectedRoute.Count -gt 0 -and -not $DistRoot) {
  throw "DistRoot is required when ExpectedRoute is provided."
}
if ($DistRoot) {
  $resolvedDist = (Resolve-Path -LiteralPath $DistRoot).Path
  foreach ($route in $ExpectedRoute) {
    if ($route -notmatch '^[a-z0-9/-]+$' -or $route.Contains("..")) {
      throw "Invalid expected route: $route"
    }
    $routeIndex = Join-Path $resolvedDist (Join-Path $route "index.html")
    if (-not (Test-Path -LiteralPath $routeIndex -PathType Leaf)) {
      throw "Expected packaged route is missing: $route"
    }
  }
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
