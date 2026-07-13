param(
  [Parameter(Mandatory = $true)][string]$ProjectRoot,
  [Parameter(Mandatory = $true)][string]$ExpectedRemoteHead,
  [string]$CandidateRef = "HEAD",
  [string]$Remote = "origin",
  [string]$Branch = "codex/service-plaza-phase1-integration",
  [string]$PolicyPath = "",
  [switch]$ExecutePush
)

$ErrorActionPreference = "Stop"

function Write-GateResult {
  param(
    [Parameter(Mandatory = $true)][string]$Status,
    [Parameter(Mandatory = $true)][AllowEmptyString()][string]$ErrorId,
    [Parameter(Mandatory = $true)][string]$Message,
    [hashtable]$Details = @{}
  )
  $result = [ordered]@{
    status = $Status
    error_id = $ErrorId
    message = $Message
    details = $Details
  }
  $result | ConvertTo-Json -Depth 6 -Compress
}

function Stop-Gate {
  param(
    [Parameter(Mandatory = $true)][string]$ErrorId,
    [Parameter(Mandatory = $true)][string]$Message,
    [hashtable]$Details = @{}
  )
  Write-GateResult -Status "blocked" -ErrorId $ErrorId -Message $Message -Details $Details
  exit 1
}

function Invoke-GitChecked {
  param([Parameter(Mandatory = $true)][string[]]$Arguments)
  $previous = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  $output = @(& git @Arguments 2>&1)
  $exitCode = $LASTEXITCODE
  $ErrorActionPreference = $previous
  [pscustomobject]@{
    ExitCode = $exitCode
    Output = @($output | ForEach-Object { $_.ToString() })
  }
}

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
  Stop-Gate -ErrorId "INTEGRATION_REPOSITORY_INVALID" -Message "ProjectRoot does not exist."
}
$root = [IO.Path]::GetFullPath($ProjectRoot)
if (-not $PolicyPath) {
  $PolicyPath = Join-Path $root "contracts\foundation\integration-push-policy.v1.json"
}
if (-not (Test-Path -LiteralPath $PolicyPath -PathType Leaf)) {
  Stop-Gate -ErrorId "INTEGRATION_REPOSITORY_INVALID" -Message "Integration push policy is missing."
}

$inside = Invoke-GitChecked -Arguments @("-C", $root, "rev-parse", "--show-toplevel")
if ($inside.ExitCode -ne 0) {
  Stop-Gate -ErrorId "INTEGRATION_REPOSITORY_INVALID" -Message "ProjectRoot is not a Git worktree."
}

$policy = Get-Content -LiteralPath $PolicyPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($policy.authority.remote -ne $Remote -or $policy.authority.branch -ne $Branch) {
  Stop-Gate -ErrorId "INTEGRATION_REPOSITORY_INVALID" -Message "Remote or branch does not match the versioned authority policy."
}
if ($ExpectedRemoteHead -notmatch "^[0-9a-fA-F]{40}$") {
  Stop-Gate -ErrorId "INTEGRATION_EXPECTED_REMOTE_INVALID" -Message "ExpectedRemoteHead must be a full 40-character commit SHA."
}
$ExpectedRemoteHead = $ExpectedRemoteHead.ToLowerInvariant()

$status = Invoke-GitChecked -Arguments @("-C", $root, "status", "--porcelain")
if ($status.ExitCode -ne 0) {
  Stop-Gate -ErrorId "INTEGRATION_REPOSITORY_INVALID" -Message "Unable to inspect worktree status."
}
if (@($status.Output | Where-Object { $_ }).Count -gt 0) {
  Stop-Gate -ErrorId "INTEGRATION_WORKTREE_DIRTY" -Message "Candidate worktree must be clean before validation or push."
}

$branchResult = Invoke-GitChecked -Arguments @("-C", $root, "symbolic-ref", "--short", "HEAD")
if ($branchResult.ExitCode -ne 0 -or $branchResult.Output.Count -ne 1) {
  Stop-Gate -ErrorId "INTEGRATION_CANDIDATE_BRANCH_INVALID" -Message "Candidate must be on a named branch."
}
$candidateBranch = $branchResult.Output[0].Trim()
if (-not $candidateBranch.StartsWith([string]$policy.candidate.allowed_branch_prefix, [StringComparison]::Ordinal)) {
  Stop-Gate -ErrorId "INTEGRATION_CANDIDATE_BRANCH_INVALID" -Message "Candidate branch is outside the approved codex/ namespace." -Details @{ branch = $candidateBranch }
}

$fetchRef = "+refs/heads/${Branch}:refs/remotes/${Remote}/${Branch}"
$fetch = Invoke-GitChecked -Arguments @("-C", $root, "fetch", "--quiet", $Remote, $fetchRef)
if ($fetch.ExitCode -ne 0) {
  Stop-Gate -ErrorId "INTEGRATION_REMOTE_UNAVAILABLE" -Message "Unable to fetch the authoritative integration branch."
}
$remoteRef = "refs/remotes/${Remote}/${Branch}"
$remoteHeadResult = Invoke-GitChecked -Arguments @("-C", $root, "rev-parse", "--verify", $remoteRef)
if ($remoteHeadResult.ExitCode -ne 0 -or $remoteHeadResult.Output.Count -ne 1) {
  Stop-Gate -ErrorId "INTEGRATION_REMOTE_UNAVAILABLE" -Message "Fetched authoritative remote ref cannot be resolved."
}
$remoteHead = $remoteHeadResult.Output[0].Trim().ToLowerInvariant()
if ($remoteHead -ne $ExpectedRemoteHead) {
  Stop-Gate -ErrorId "INTEGRATION_REMOTE_HEAD_CHANGED" -Message "Authoritative remote HEAD differs from the caller's expected lease." -Details @{ expected = $ExpectedRemoteHead; actual = $remoteHead }
}

$candidateResult = Invoke-GitChecked -Arguments @("-C", $root, "rev-parse", "--verify", "${CandidateRef}^{commit}")
if ($candidateResult.ExitCode -ne 0 -or $candidateResult.Output.Count -ne 1) {
  Stop-Gate -ErrorId "INTEGRATION_CANDIDATE_INVALID" -Message "CandidateRef cannot be resolved to a commit."
}
$candidateHead = $candidateResult.Output[0].Trim().ToLowerInvariant()

$counts = Invoke-GitChecked -Arguments @("-C", $root, "rev-list", "--left-right", "--count", "${remoteHead}...${candidateHead}")
if ($counts.ExitCode -ne 0 -or $counts.Output.Count -ne 1) {
  Stop-Gate -ErrorId "INTEGRATION_CANDIDATE_INVALID" -Message "Unable to calculate ahead and behind counts."
}
$parts = @($counts.Output[0].Trim() -split "\s+")
if ($parts.Count -ne 2) {
  Stop-Gate -ErrorId "INTEGRATION_CANDIDATE_INVALID" -Message "Unexpected ahead and behind count format."
}
$behind = [int]$parts[0]
$ahead = [int]$parts[1]
if ($behind -gt [int]$policy.candidate.max_behind_count) {
  if ($ahead -eq 0) {
    Stop-Gate -ErrorId "INTEGRATION_CANDIDATE_BEHIND" -Message "Candidate is behind the authoritative remote branch." -Details @{ behind = $behind; ahead = $ahead }
  }
  Stop-Gate -ErrorId "INTEGRATION_REMOTE_NOT_ANCESTOR" -Message "Candidate and authoritative remote have diverged." -Details @{ behind = $behind; ahead = $ahead; remote = $remoteHead; candidate = $candidateHead }
}

$ancestor = Invoke-GitChecked -Arguments @("-C", $root, "merge-base", "--is-ancestor", $remoteHead, $candidateHead)
if ($ancestor.ExitCode -ne 0) {
  Stop-Gate -ErrorId "INTEGRATION_REMOTE_NOT_ANCESTOR" -Message "Candidate does not contain the authoritative remote history." -Details @{ remote = $remoteHead; candidate = $candidateHead }
}

$details = @{
  remote = $Remote
  branch = $Branch
  expected_remote_head = $ExpectedRemoteHead
  actual_remote_head = $remoteHead
  candidate_head = $candidateHead
  candidate_branch = $candidateBranch
  behind = $behind
  ahead = $ahead
  lease = "refs/heads/${Branch}:${ExpectedRemoteHead}"
}

if (-not $ExecutePush) {
  Write-GateResult -Status "ready" -ErrorId "" -Message "Candidate is fresh and lease-safe for authoritative integration push." -Details $details
  exit 0
}

$leaseCheck = Invoke-GitChecked -Arguments @("-C", $root, "ls-remote", "--heads", $Remote, "refs/heads/${Branch}")
if ($leaseCheck.ExitCode -ne 0 -or $leaseCheck.Output.Count -ne 1) {
  Stop-Gate -ErrorId "INTEGRATION_REMOTE_UNAVAILABLE" -Message "Unable to re-read remote HEAD immediately before push."
}
$leaseRemoteHead = (@($leaseCheck.Output[0].Trim() -split "\s+")[0]).ToLowerInvariant()
if ($leaseRemoteHead -ne $ExpectedRemoteHead) {
  Stop-Gate -ErrorId "INTEGRATION_REMOTE_HEAD_CHANGED" -Message "Remote HEAD changed after validation and before push." -Details @{ expected = $ExpectedRemoteHead; actual = $leaseRemoteHead }
}

$leaseArgument = "--force-with-lease=refs/heads/${Branch}:${ExpectedRemoteHead}"
$refspec = "${candidateHead}:refs/heads/${Branch}"
$push = Invoke-GitChecked -Arguments @("-C", $root, "push", "--porcelain", $leaseArgument, $Remote, $refspec)
if ($push.ExitCode -ne 0) {
  Stop-Gate -ErrorId "INTEGRATION_LEASE_PUSH_FAILED" -Message "Lease-protected push was rejected; no retry or force fallback is allowed."
}

$after = Invoke-GitChecked -Arguments @("-C", $root, "ls-remote", "--heads", $Remote, "refs/heads/${Branch}")
if ($after.ExitCode -ne 0 -or $after.Output.Count -ne 1) {
  Stop-Gate -ErrorId "INTEGRATION_REMOTE_UNAVAILABLE" -Message "Unable to verify remote HEAD after push."
}
$afterHead = (@($after.Output[0].Trim() -split "\s+")[0]).ToLowerInvariant()
if ($afterHead -ne $candidateHead) {
  Stop-Gate -ErrorId "INTEGRATION_POST_PUSH_MISMATCH" -Message "Remote HEAD does not equal the validated candidate after push." -Details @{ expected = $candidateHead; actual = $afterHead }
}
$details["pushed_head"] = $afterHead
Write-GateResult -Status "pushed" -ErrorId "" -Message "Lease-protected authoritative integration push completed and verified." -Details $details
