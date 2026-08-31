param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('FreshReady', 'PreserveReady', 'CleanupReady')]
  [string]$Phase,

  [Parameter(Mandatory = $true)]
  [ValidatePattern('^\d{4}$')]
  [string]$RunId,

  [Parameter(Mandatory = $true)]
  [ValidateSet('NO-SKILL', '00-SUPPLIED', '01-V1-CANDIDATE', '02-V2-GRAPH')]
  [string]$SkillVersion,

  [string]$Baseline = 'cd393ddd60548823dabd6875060247693a22c1be',

  [string]$ActivePath,

  [string]$MotherPath
)

$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
if (-not $ActivePath) {
  $ActivePath = Join-Path $root 'ACTIVE\ShingleFile-main'
}
if (-not $MotherPath) {
  $MotherPath = Join-Path $root 'MOTHER\ShingleFile-main.git'
}

$skillPath = Join-Path $env:USERPROFILE '.cursor\skills-cursor\layered-codebase-architecture'
$cursorProject = Join-Path $env:USERPROFILE '.cursor\projects\d-Downloads-Skill-Evaluation-Lab-ACTIVE-ShingleFile-main'
$errors = @()
$warnings = @()
$notes = @()

function Add-Error([string]$message) {
  $script:errors += $message
}

function Add-Warning([string]$message) {
  $script:warnings += $message
}

function Add-Note([string]$message) {
  $script:notes += $message
}

function Read-Text([string]$path) {
  if (-not (Test-Path -LiteralPath $path)) {
    return $null
  }
  return Get-Content -Raw -LiteralPath $path
}

function Get-RunIndexRows([string]$runId) {
  $rows = @()
  $files = Get-ChildItem -LiteralPath (Join-Path $root 'EXPERIMENTS') -Filter 'RUN-INDEX.md' -Recurse
  foreach ($file in $files) {
    $rel = Resolve-Path -LiteralPath $file.FullName -Relative
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
      if ($line -match ('^\|\s*`?' + [regex]::Escape($runId) + '`?\s*\|')) {
        $rows += [pscustomobject]@{ Path = $rel; Line = $line }
      }
    }
  }
  return @($rows)
}

function Get-RunIndexStatus([string]$line) {
  $parts = $line.Trim('|') -split '\|'
  if ($parts.Count -lt 6) {
    return $null
  }
  return $parts[$parts.Count - 1].Trim()
}

function Get-FileHashMap([string]$path) {
  $map = @{}
  if (-not (Test-Path -LiteralPath $path)) {
    return $map
  }
  Get-ChildItem -LiteralPath $path -File | Sort-Object Name | ForEach-Object {
    $map[$_.Name] = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
  }
  return $map
}

function Compare-SkillArtifact([string]$version) {
  if ($version -eq 'NO-SKILL') {
    if (Test-Path -LiteralPath $skillPath) {
      Add-Error "Expected no global skill folder, but found $skillPath"
    } else {
      Add-Note 'Global skill folder is absent for no-skill arm.'
    }
    return
  }

  if (-not (Test-Path -LiteralPath $skillPath)) {
    Add-Error "Expected global skill folder for $version, but it is absent."
    return
  }

  $source = Join-Path $root "SKILLS\layered-codebase-architecture\$version"
  if (-not (Test-Path -LiteralPath $source)) {
    Add-Error "Missing frozen skill artifact source: $source"
    return
  }

  $sourceHashes = Get-FileHashMap $source
  $runtimeHashes = Get-FileHashMap $skillPath
  $sourceNames = @($sourceHashes.Keys | Sort-Object)
  $runtimeNames = @($runtimeHashes.Keys | Sort-Object)
  if (($sourceNames -join '|') -ne ($runtimeNames -join '|')) {
    Add-Error "Runtime skill files do not match $version file set."
    return
  }
  foreach ($name in $sourceNames) {
    if ($sourceHashes[$name] -ne $runtimeHashes[$name]) {
      Add-Error "Runtime skill hash mismatch for ${name}: $($runtimeHashes[$name]) != $($sourceHashes[$name])"
    }
  }
  Add-Note "Global skill folder matches $version hashes."
}

function Check-CurrentState([string]$runId, [string]$field) {
  $current = Read-Text (Join-Path $root 'CURRENT-STATE.md')
  if ($null -eq $current) {
    Add-Error 'Missing CURRENT-STATE.md'
    return
  }
  $pattern = [regex]::Escape($field) + ':\s*`' + [regex]::Escape($runId) + '`'
  if ($current -notmatch $pattern) {
    Add-Error "CURRENT-STATE.md does not set $field to $runId."
  } else {
    Add-Note "CURRENT-STATE.md sets $field to $runId."
  }
}

function Check-CanonicalTargets([string]$runId, [string]$expectedRunIndexStatus) {
  $rows = @(Get-RunIndexRows $runId)
  if ($rows.Count -ne 1) {
    Add-Error "Run index should contain exactly one row for $runId; found $($rows.Count)."
  } else {
    $status = Get-RunIndexStatus $rows[0].Line
    if ($status -ne $expectedRunIndexStatus) {
      Add-Error "Run index row for $runId should be $expectedRunIndexStatus; found $status."
    } else {
      Add-Note "Run index row for $runId is $status."
    }
  }

  $evidencePath = Join-Path $root "EVIDENCE\$runId"
  $historyPath = Join-Path $root "DEVELOPMENT-HISTORY\$runId.md"
  $archiveMatches = @(Get-ChildItem -LiteralPath (Join-Path $root 'ARCHIVES\local') -Filter "run-$runId-*.zip" -File -ErrorAction SilentlyContinue)
  $dataText = Read-Text (Join-Path $root 'DATA\runs.json')

  if ($expectedRunIndexStatus -eq 'planned') {
    if (Test-Path -LiteralPath $evidencePath) { Add-Error "Evidence already exists for planned run: $evidencePath" }
    if (Test-Path -LiteralPath $historyPath) { Add-Error "Development history already exists for planned run: $historyPath" }
    if ($archiveMatches.Count -gt 0) { Add-Error "Local archive already exists for planned run $runId." }
    if ($dataText -match ('"run_id"\s*:\s*"' + [regex]::Escape($runId) + '"')) {
      Add-Error "DATA/runs.json already contains $runId."
    }
  } else {
    if (-not (Test-Path -LiteralPath $evidencePath)) { Add-Error "Missing preserved evidence path: $evidencePath" }
    if (-not (Test-Path -LiteralPath $historyPath)) { Add-Error "Missing preserved development history: $historyPath" }
    if ($archiveMatches.Count -eq 0) { Add-Error "Missing local archive for preserved run $runId." }
    if ($dataText -notmatch ('"run_id"\s*:\s*"' + [regex]::Escape($runId) + '"')) {
      Add-Error "DATA/runs.json does not contain preserved run $runId."
    }
  }
}

function Check-Mother {
  if (-not (Test-Path -LiteralPath $MotherPath)) {
    Add-Error "Missing Mother repository: $MotherPath"
    return
  }
  $head = (& git --git-dir=$MotherPath rev-parse HEAD).Trim()
  if ($head -ne $Baseline) {
    Add-Error "Mother HEAD $head does not match baseline $Baseline."
  } else {
    Add-Note "Mother HEAD matches baseline $Baseline."
  }
}

function Check-Active([bool]$mustBeClean, [bool]$subjectCursorMustBeAbsent) {
  if (-not (Test-Path -LiteralPath $ActivePath)) {
    Add-Error "Missing Active checkout: $ActivePath"
    return
  }
  $head = (& git -C $ActivePath rev-parse HEAD).Trim()
  if ($head -ne $Baseline) {
    Add-Error "Active HEAD $head does not match baseline $Baseline."
  } else {
    Add-Note 'Active HEAD matches baseline.'
  }

  $fetchRemote = (& git -C $ActivePath remote get-url origin).Trim()
  $pushRemote = (& git -C $ActivePath config --get remote.origin.pushurl)
  if ($fetchRemote -ne '../../MOTHER/ShingleFile-main.git') {
    Add-Warning "Active fetch remote is $fetchRemote; expected ../../MOTHER/ShingleFile-main.git"
  }
  if (($pushRemote -join '').Trim() -ne 'WORKPLACE-MOTHER-PUSH-DISABLED') {
    Add-Error 'Active push remote is not WORKPLACE-MOTHER-PUSH-DISABLED.'
  } else {
    Add-Note 'Active push remote is disabled.'
  }

  $status = @(& git -C $ActivePath status --porcelain=v1)
  if ($mustBeClean -and $status.Count -gt 0) {
    Add-Error "Active should be clean for $Phase, but has $($status.Count) status rows."
  }
  if (-not $mustBeClean) {
    Add-Note "Active status rows: $($status.Count)"
    $untracked = @(& git -C $ActivePath ls-files --others --exclude-standard)
    Add-Note "Active untracked rows: $($untracked.Count). Capture these separately; tracked diff will not include them."
  }

  $subjectCursor = Test-Path -LiteralPath (Join-Path $ActivePath '.cursor')
  if ($subjectCursorMustBeAbsent -and $subjectCursor) {
    Add-Error 'Subject repository has .cursor before launch; this contaminates harness attribution.'
  }
  if (-not $subjectCursorMustBeAbsent -and $subjectCursor) {
    Add-Warning 'Subject repository has .cursor; preserve it as model-created/untracked state if present after the run.'
  }
}

function Check-CursorTraceCandidates {
  $traceRoot = Join-Path $cursorProject 'agent-transcripts'
  if (-not (Test-Path -LiteralPath $traceRoot)) {
    Add-Warning "No Cursor transcript root found at $traceRoot"
    return
  }
  $candidates = @(Get-ChildItem -LiteralPath $traceRoot -Recurse -File -Filter '*.jsonl' | Sort-Object LastWriteTime -Descending | Select-Object -First 5)
  if ($candidates.Count -eq 0) {
    Add-Warning 'No Cursor JSONL transcript candidates found.'
    return
  }
  Add-Note 'Recent Cursor transcript candidates:'
  foreach ($candidate in $candidates) {
    Add-Note ("  {0} {1}" -f $candidate.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'), $candidate.FullName)
  }
}

function Check-CursorLock {
  $windows = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -eq 'Cursor' -and $_.MainWindowTitle -like '*ShingleFile-main*' })
  if ($windows.Count -gt 0) {
    $titles = ($windows | ForEach-Object { "$($_.Id):$($_.MainWindowTitle)" }) -join '; '
    if ($Phase -eq 'CleanupReady') {
      Add-Error "Close Cursor before moving Active. Open windows: $titles"
    } else {
      Add-Warning "Cursor windows for ShingleFile-main are open: $titles"
    }
  } else {
    Add-Note 'No visible Cursor ShingleFile-main window detected.'
  }
}

Check-Mother
Compare-SkillArtifact $SkillVersion

switch ($Phase) {
  'FreshReady' {
    Check-CurrentState $RunId 'Next global run'
    Check-CanonicalTargets $RunId 'planned'
    Check-Active -mustBeClean $true -subjectCursorMustBeAbsent $true
    Check-CursorLock
  }
  'PreserveReady' {
    Check-CurrentState $RunId 'Next global run'
    Check-CanonicalTargets $RunId 'planned'
    Check-Active -mustBeClean $false -subjectCursorMustBeAbsent $false
    Check-CursorTraceCandidates
    Add-Note 'If git diff --check emits no rows, create an explicit empty diff-check.txt evidence file.'
  }
  'CleanupReady' {
    Check-CurrentState $RunId 'Current completed global run'
    Check-CanonicalTargets $RunId 'preserved'
    Check-Active -mustBeClean $false -subjectCursorMustBeAbsent $false
    Check-CursorLock
    Add-Note 'Archive must already exist and verify before cleanup. Use [System.IO.Directory]::Move for same-drive Active retirement.'
  }
}

Write-Host "phase=$Phase"
Write-Host "run_id=$RunId"
Write-Host "skill_version=$SkillVersion"
foreach ($note in $notes) {
  Write-Host "NOTE: $note"
}
foreach ($warning in $warnings) {
  Write-Warning $warning
}
if ($errors.Count -gt 0) {
  foreach ($errorMessage in $errors) {
    Write-Error $errorMessage -ErrorAction Continue
  }
  exit 1
}
Write-Host 'CHECKPOINT_OK'
