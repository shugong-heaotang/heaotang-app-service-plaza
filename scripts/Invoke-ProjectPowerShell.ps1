param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$Script,

  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$ScriptArguments
)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$repoRoot = Split-Path $PSScriptRoot -Parent
$target = if ([System.IO.Path]::IsPathRooted($Script)) {
  $Script
} else {
  Join-Path $repoRoot $Script
}

$resolvedTarget = (Resolve-Path -LiteralPath $target).Path
& $resolvedTarget @ScriptArguments
exit $LASTEXITCODE
