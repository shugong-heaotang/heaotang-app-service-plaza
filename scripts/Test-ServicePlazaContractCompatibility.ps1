param(
  [string]$BaseRef = ""
)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$repoRoot = Split-Path $PSScriptRoot -Parent
$checker = Join-Path $PSScriptRoot "check_service_plaza_contract_compatibility.py"
$tests = Join-Path $PSScriptRoot "tests"

function Test-GitObject {
  param([Parameter(Mandatory = $true)][string]$ObjectName)

  $previousErrorActionPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try {
    & git cat-file -e $ObjectName 2>$null
    return $LASTEXITCODE -eq 0
  } finally {
    $ErrorActionPreference = $previousErrorActionPreference
  }
}

function Test-GitCommit {
  param([Parameter(Mandatory = $true)][string]$Revision)

  $previousErrorActionPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try {
    & git rev-parse --verify "$Revision^{commit}" 2>$null | Out-Null
    return $LASTEXITCODE -eq 0
  } finally {
    $ErrorActionPreference = $previousErrorActionPreference
  }
}

Push-Location $repoRoot
try {
  & python -B -X utf8 -m unittest discover -s $tests -p "test_service_plaza_contract_compatibility.py" -v
  if ($LASTEXITCODE -ne 0) {
    throw "Service Plaza compatibility gate tests failed."
  }

  if ([string]::IsNullOrWhiteSpace($BaseRef) -or $BaseRef -match "^0+$") {
    if (Test-GitCommit -Revision "HEAD^") {
      $BaseRef = "HEAD^"
    } else {
      Write-Host "Compatibility unit tests passed; no earlier Git revision exists for a contract diff."
      return
    }
  }

  if (-not (Test-GitCommit -Revision $BaseRef)) {
    throw "Compatibility base revision is unavailable: $BaseRef"
  }

  $contracts = @(
    @{ Path = "contracts/service-plaza/service-plaza-actions.v1.json"; Kind = "action-baseline" },
    @{ Path = "contracts/service-plaza/service-plaza-action.schema.json"; Kind = "json-schema" },
    @{ Path = "contracts/service-plaza/service-manifest.schema.json"; Kind = "json-schema" }
  )

  foreach ($contract in $contracts) {
    if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $contract.Path))) {
      throw "Current contract file is missing: $($contract.Path)"
    }

    if (-not (Test-GitObject -ObjectName "$BaseRef`:$($contract.Path)")) {
      Write-Host "Compatibility baseline does not contain $($contract.Path); treating it as a newly introduced contract."
      continue
    }

    & python -B -X utf8 $checker $contract.Path $contract.Path --old-git-ref $BaseRef --kind $contract.Kind
    if ($LASTEXITCODE -ne 0) {
      throw "Backward compatibility failed for $($contract.Path)."
    }
  }
} finally {
  Pop-Location
}

Write-Host "Service Plaza contract compatibility gate passed."
