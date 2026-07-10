param(
  [switch]$Quiet
)

$ErrorActionPreference = "Stop"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

[Console]::InputEncoding = $utf8NoBom
[Console]::OutputEncoding = $utf8NoBom
Set-Variable -Name OutputEncoding -Value $utf8NoBom -Scope Global

$env:PYTHONIOENCODING = "utf-8"
$env:LANG = "C.UTF-8"
$env:LC_ALL = "C.UTF-8"
$env:GIT_PAGER = "cat"

if ($env:OS -eq "Windows_NT") {
  $chcp = Get-Command chcp.com -ErrorAction SilentlyContinue
  if ($chcp) {
    & $chcp.Source 65001 | Out-Null
  }
}

$PSDefaultParameterValues["Out-File:Encoding"] = "utf8"
$PSDefaultParameterValues["Set-Content:Encoding"] = "utf8"
$PSDefaultParameterValues["Add-Content:Encoding"] = "utf8"
$PSDefaultParameterValues["Export-Csv:Encoding"] = "utf8"

if (-not $Quiet) {
  Write-Host "PowerShell UTF-8 environment initialized."
}
