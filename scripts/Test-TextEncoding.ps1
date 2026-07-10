param(
  [string[]]$AdditionalRoots = @("C:\Users\shugo\Documents\heaotang-main\backend-go")
)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "Initialize-PowerShellUtf8.ps1") -Quiet

$repoRoot = Split-Path $PSScriptRoot -Parent
$strictUtf8 = New-Object System.Text.UTF8Encoding($false, $true)
$textExtensions = @(
  ".md", ".json", ".yml", ".yaml", ".js", ".jsx", ".ts", ".tsx",
  ".css", ".scss", ".html", ".go", ".py", ".sh", ".ps1", ".psm1", ".psd1"
)
$powerShellExtensions = @(".ps1", ".psm1", ".psd1")
$ignoredDirectories = @(".git", "node_modules", "dist", "build", "coverage")
$mojibakePatterns = @(
  "鏈嶅姟", "鏂囦欢", "椤圭洰", "鎺ㄨ繘", "闂ㄧ", "锛?", "銆?", "鈥?",
  "闁崇", "闁冲", "妤犵", "閹般", "濞ｅ", "婵炶", "�?"
)
$issues = New-Object System.Collections.Generic.List[string]

$files = New-Object System.Collections.Generic.List[System.IO.FileInfo]
$pendingDirectories = New-Object System.Collections.Generic.Stack[System.IO.DirectoryInfo]
foreach ($root in @($repoRoot) + $AdditionalRoots) {
  if (Test-Path -LiteralPath $root) {
    $pendingDirectories.Push((Get-Item -LiteralPath $root))
  }
}

while ($pendingDirectories.Count -gt 0) {
  $directory = $pendingDirectories.Pop()
  foreach ($childDirectory in Get-ChildItem -LiteralPath $directory.FullName -Directory) {
    if ($ignoredDirectories -notcontains $childDirectory.Name) {
      $pendingDirectories.Push($childDirectory)
    }
  }

  foreach ($file in Get-ChildItem -LiteralPath $directory.FullName -File) {
    if ($textExtensions -contains $file.Extension.ToLowerInvariant()) {
      $files.Add($file)
    }
  }
}

foreach ($file in $files) {
  $relativePath = if ($file.FullName.StartsWith($repoRoot, [StringComparison]::OrdinalIgnoreCase)) {
    $file.FullName.Substring($repoRoot.Length).TrimStart("\", "/")
  } else {
    $file.FullName
  }
  $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
  $hasBom = $bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF
  $isPowerShell = $powerShellExtensions -contains $file.Extension.ToLowerInvariant()

  if ($isPowerShell -and -not $hasBom) {
    $issues.Add("PowerShell file must use UTF-8 BOM: $relativePath")
  }
  if (-not $isPowerShell -and $hasBom) {
    $issues.Add("Cross-platform text file must use UTF-8 without BOM: $relativePath")
  }

  try {
    $text = $strictUtf8.GetString($bytes)
  } catch {
    $issues.Add("Invalid UTF-8 byte sequence: $relativePath")
    continue
  }

  if ($file.Name -ne "Test-TextEncoding.ps1") {
    foreach ($pattern in $mojibakePatterns) {
      if ($text.Contains($pattern)) {
        $issues.Add("Possible mojibake '$pattern': $relativePath")
        break
      }
    }
  }

  if ($isPowerShell) {
    $tokens = $null
    $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile(
      $file.FullName,
      [ref]$tokens,
      [ref]$parseErrors
    ) | Out-Null
    if ($parseErrors.Count -gt 0) {
      $message = ($parseErrors | Select-Object -First 2 | ForEach-Object Message) -join " | "
      $issues.Add("PowerShell parse error in ${relativePath}: $message")
    }
  }
}

if ($issues.Count -gt 0) {
  $issues | ForEach-Object { [Console]::Error.WriteLine($_) }
  exit 1
}

Write-Host "Text encoding check passed: $($files.Count) files."
