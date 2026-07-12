param()

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$repoRoot = Split-Path $PSScriptRoot -Parent
$appRoot = Join-Path $repoRoot "app"
$distRoot = Join-Path $appRoot "dist"
$contractSources = @{
  "service-manifest.v1.schema.json" = Join-Path $repoRoot "contracts\service-plaza\service-manifest.schema.json"
  "service-plaza-action.v1.schema.json" = Join-Path $repoRoot "contracts\service-plaza\service-plaza-action.schema.json"
  "service-plaza-actions.v1.json" = Join-Path $repoRoot "contracts\service-plaza\service-plaza-actions.v1.json"
}

# Vite loads only one matching config file. A stale JavaScript build artifact can
# shadow vite.config.ts and silently discard the deployment base path.
$shadowConfigs = @(
  "vite.config.js",
  "vite.config.mjs",
  "vite.config.cjs"
) | ForEach-Object { Join-Path $appRoot $_ } | Where-Object { Test-Path -LiteralPath $_ }

if ($shadowConfigs.Count -gt 0) {
  throw "Stale Vite config shadows vite.config.ts: $($shadowConfigs -join ', '). Remove the generated config at its source before building."
}

Push-Location $appRoot
try {
  & npm.cmd run build:test-server
  if ($LASTEXITCODE -ne 0) {
    throw "Frontend test-server build failed."
  }
} finally {
  Pop-Location
}

$contractTarget = Join-Path $distRoot "contracts\service-plaza"
New-Item -ItemType Directory -Path $contractTarget -Force | Out-Null
foreach ($targetName in $contractSources.Keys) {
  $source = $contractSources[$targetName]
  if (-not (Test-Path -LiteralPath $source)) {
    throw "Service Plaza contract file is missing: $source"
  }
  Copy-Item -LiteralPath $source -Destination (Join-Path $contractTarget $targetName) -Force
}

$routeDirectories = @(
  "services",
  "services/life-navigation",
  "services/club-alliance",
  "services/club-alliance/self-created",
  "services/club-alliance/self-created/applications",
  "services/health-manager"
)

foreach ($route in $routeDirectories) {
  $targetDirectory = Join-Path $distRoot $route
  New-Item -ItemType Directory -Path $targetDirectory -Force | Out-Null
  Copy-Item -LiteralPath (Join-Path $distRoot "index.html") -Destination (Join-Path $targetDirectory "index.html") -Force
}

$manifest = [ordered]@{
  built_at = [DateTime]::UtcNow.ToString("o")
  public_base = "/app/service-plaza/"
  routes = $routeDirectories
  assets = @(Get-ChildItem -LiteralPath (Join-Path $distRoot "assets") -File | Select-Object -ExpandProperty Name)
}
$manifestJson = $manifest | ConvertTo-Json -Depth 4
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path $distRoot "deployment-manifest.json"), $manifestJson + "`n", $utf8NoBom)

Write-Host "Service Plaza test-server package built at $distRoot"
