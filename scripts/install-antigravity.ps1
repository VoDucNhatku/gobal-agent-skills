<#
Pilot-only Direct/Global installer for Windows PowerShell 5.1.
The temporary always_on pilot rule affects other chats while installed.
Full rollout is withheld until the real IDE canary passes.
Testing only: GOBAL_INSTALL_TEST_FAIL_AFTER=N injects a caught write failure;
GOBAL_INSTALL_TEST_INTERRUPT_AFTER=N exits before recovery, and
GOBAL_INSTALL_TEST_INTERRUPT_BEFORE_COMMIT=1 exits after ownership replacement.
These markers are refused outside an explicitly selected temporary profile.
#>
[CmdletBinding()]
param(
    [string]$SourcePath = '',
    [string]$ProfileRoot = $env:USERPROFILE,
    [switch]$Pilot,
    [switch]$Uninstall,
    [switch]$DryRun,
    [switch]$Force,
    [switch]$Recover
)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($SourcePath)) { $SourcePath = Split-Path -Parent $PSScriptRoot }
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
if (-not $Pilot) {
    Write-Warning 'Full rollout is not released. Use -Pilot for the namespaced canary only.'
    exit 1
}

function Assert-NoReparseAncestors([string]$Path) {
    $cursor = [IO.Path]::GetFullPath($Path)
    while ($cursor) {
        $item = Get-Item -LiteralPath $cursor -Force -ErrorAction SilentlyContinue
        if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Reparse point is forbidden: $cursor"
        }
        $parent = [IO.Path]::GetDirectoryName($cursor)
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
}

function Assert-Contained([string]$Root, [string]$Path) {
    $rootFull = [IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
    $pathFull = [IO.Path]::GetFullPath($Path)
    if (($pathFull -ne $rootFull) -and -not $pathFull.StartsWith($rootFull + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path escapes approved root: $Path"
    }
    Assert-NoReparseAncestors $pathFull
    return $pathFull
}

function Assert-ManagedRelative([string]$Relative) {
    if ($Relative -cnotmatch '^(skills/admin-evidence-pilot/.+|rules/admin-evidence-pilot\.md)$') {
        throw "Path is outside pilot ownership: $Relative"
    }
    foreach ($segment in $Relative.Split('/')) {
        if (($segment -in @('', '.', '..')) -or ($segment -match '[\x00-\x1f<>:"|?*\\]') -or
            $segment.EndsWith('.') -or $segment.EndsWith(' ') -or
            $segment -match '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$') {
            throw "Invalid managed path: $Relative"
        }
    }
}

function Get-Hash([string]$Path) {
    Assert-NoReparseAncestors $Path
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Expected file: $Path" }
    $stream = [IO.File]::OpenRead($Path)
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose(); $stream.Dispose() }
}

function Assert-UniqueJsonKeys([string]$Text) {
    # ConvertFrom-Json on Windows PowerShell silently keeps the last duplicate.
    # Track property names per object; quoted braces/colons remain string tokens.
    # ConvertFrom-Json subsequently validates the complete JSON grammar.
    $tokens = [regex]::Matches($Text, '"(?:[^"\\]|\\.)*"|[{}\[\]:,]')
    $objects = New-Object 'System.Collections.Generic.Stack[object]'
    for ($index = 0; $index -lt $tokens.Count; $index++) {
        $token = $tokens[$index].Value
        if ($token -eq '{') {
            $keys = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
            $objects.Push($keys)
        } elseif ($token -eq '[') {
            $objects.Push($null)
        } elseif ($token -in @('}', ']')) {
            if ($objects.Count -eq 0) { throw 'Invalid JSON nesting' }
            $null = $objects.Pop()
        } elseif ($token.StartsWith('"') -and $index + 1 -lt $tokens.Count -and $tokens[$index + 1].Value -eq ':') {
            if ($objects.Count -eq 0 -or $null -eq $objects.Peek()) { throw 'Invalid JSON property placement' }
            $key = $token | ConvertFrom-Json
            if (-not $objects.Peek().Add($key)) { throw "Duplicate JSON key: $key" }
        }
    }
}

function Read-Json([string]$Path) {
    Assert-NoReparseAncestors $Path
    $text = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
    Assert-UniqueJsonKeys $text
    return ($text | ConvertFrom-Json)
}

function Convert-FileMap($Files) {
    if (-not ($Files -is [PSCustomObject])) { throw 'files must be a JSON object' }
    $map = [ordered]@{}
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
    foreach ($property in $Files.PSObject.Properties) {
        Assert-ManagedRelative $property.Name
        if (-not $seen.Add($property.Name)) { throw "Duplicate file path: $($property.Name)" }
        if (-not ($property.Value -is [string]) -or $property.Value -notmatch '^[a-fA-F0-9]{64}$') {
            throw "Invalid SHA256: $($property.Name)"
        }
        $map[$property.Name] = $property.Value.ToLowerInvariant()
    }
    return ,$map
}

function Get-SourceFiles([string]$Root, [string]$Directory) {
    foreach ($item in Get-ChildItem -LiteralPath $Directory -Force) {
        $safe = Assert-Contained $Root $item.FullName
        if ($item.PSIsContainer) { Get-SourceFiles $Root $safe }
        else { $safe }
    }
}

function Read-Payload([string]$Root) {
    $manifestPath = Assert-Contained $Root (Join-Path $Root 'manifest.json')
    $manifest = Read-Json $manifestPath
    if (-not ($manifest.schema_version -is [int]) -or $manifest.schema_version -ne 1) { throw 'Unsupported pilot manifest schema_version' }
    $files = Convert-FileMap $manifest.files
    foreach ($required in @('skills/admin-evidence-pilot/SKILL.md', 'rules/admin-evidence-pilot.md')) {
        if (-not $files.Contains($required)) { throw "Incomplete pilot manifest: $required" }
    }
    foreach ($relative in $files.Keys) {
        $sourceFile = Assert-Contained $Root (Join-Path $Root $relative)
        if ((Get-Hash $sourceFile) -ne $files[$relative]) { throw "Source hash mismatch: $relative" }
    }
    $actual = @(Get-SourceFiles $Root $Root | Where-Object { $_ -ne $manifestPath })
    if ($actual.Count -ne $files.Count) { throw 'Source file inventory differs from manifest' }
    foreach ($sourceFile in $actual) {
        $relative = $sourceFile.Substring($Root.TrimEnd('\').Length + 1).Replace('\', '/')
        if (-not $files.Contains($relative)) { throw "Unlisted source file: $relative" }
    }
    return ,$files
}

function Ensure-Directory([string]$Path) {
    $safe = Assert-Contained $profilePath $Path
    $null = [IO.Directory]::CreateDirectory($safe)
}

function Write-Json([string]$Path, $Value) {
    $safe = Assert-Contained $profilePath $Path
    Ensure-Directory ([IO.Path]::GetDirectoryName($safe))
    $temporary = Assert-Contained $profilePath ($safe + '.' + [guid]::NewGuid().ToString('N') + '.tmp')
    [IO.File]::WriteAllText($temporary, ($Value | ConvertTo-Json -Depth 15), (New-Object Text.UTF8Encoding($false)))
    if ([IO.File]::Exists($safe)) { [IO.File]::Replace($temporary, $safe, [System.Management.Automation.Language.NullString]::Value) }
    else { [IO.File]::Move($temporary, $safe) }
}

function Read-Ownership {
    if (-not (Test-Path -LiteralPath $ownershipPath)) { return ,([ordered]@{}) }
    $state = Read-Json $ownershipPath
    if (-not ($state.schema_version -is [int]) -or ($state.schema_version -ne 1) -or ($state.scope -ne 'pilot')) { throw 'Invalid pilot ownership schema' }
    return ,(Convert-FileMap $state.files)
}

function Get-Operations($Owned, $Desired) {
    $operations = @()
    foreach ($relative in @(@($Owned.Keys) + @($Desired.Keys) | Sort-Object -Unique)) {
        Assert-ManagedRelative $relative
        $target = Assert-Contained $profilePath (Join-Path $configPath $relative)
        $before = Get-Hash $target
        if ($Owned.Contains($relative) -and $before -ne $Owned[$relative] -and -not $Force) {
            throw "Owned file drift requires -Force and backup: $relative"
        }
        if (-not $Owned.Contains($relative) -and $before -and -not $Force) {
            throw "Unmanaged collision requires -Force: $relative"
        }
        $after = $null
        if ($Desired.Contains($relative)) { $after = $Desired[$relative] }
        if ($before -ne $after) {
            $operations += [ordered]@{ path = $relative; before_hash = $before; after_hash = $after }
        }
    }
    return ,$operations
}

function Put-File([string]$Staged, [string]$Target) {
    $null = Assert-Contained $profilePath $Staged
    $null = Assert-Contained $profilePath $Target
    Ensure-Directory ([IO.Path]::GetDirectoryName($Target))
    if ([IO.File]::Exists($Target)) { [IO.File]::Replace($Staged, $Target, [System.Management.Automation.Language.NullString]::Value) }
    else { [IO.File]::Move($Staged, $Target) }
}

function Invoke-TestFault([int]$OperationCount) {
    if ($env:GOBAL_INSTALL_TEST_FAIL_AFTER -and $OperationCount -eq [int]$env:GOBAL_INSTALL_TEST_FAIL_AFTER) {
        throw "Injected failure after $OperationCount operations"
    }
    if ($env:GOBAL_INSTALL_TEST_INTERRUPT_AFTER -and $OperationCount -eq [int]$env:GOBAL_INSTALL_TEST_INTERRUPT_AFTER) {
        [Environment]::Exit(97)
    }
}

function Assert-Recoverable($Journal) {
    if (-not ($Journal.schema_version -is [int]) -or ($Journal.schema_version -ne 1) -or ($Journal.scope -ne 'pilot') -or
        $Journal.id -notmatch '^[a-fA-F0-9]{8}(-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}$' -or
        $Journal.status -ne 'applying' -or -not ($Journal.entries -is [array])) {
        throw 'Invalid recovery journal schema'
    }
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
    foreach ($entry in @($Journal.entries)) {
        if (-not ($entry.path -is [string]) -or -not $seen.Add($entry.path)) { throw 'Invalid recovery journal entry' }
        foreach ($hash in @($entry.before_hash, $entry.after_hash)) {
            if ($null -ne $hash -and (-not ($hash -is [string]) -or $hash -notmatch '^[a-fA-F0-9]{64}$')) {
                throw 'Invalid recovery journal hash'
            }
        }
        if ($entry.before_hash -eq $entry.after_hash) { throw 'Invalid empty journal operation' }
    }
    foreach ($hash in @($Journal.ownership_before_hash, $Journal.ownership_after_hash)) {
        if ($null -ne $hash -and (-not ($hash -is [string]) -or $hash -notmatch '^[a-fA-F0-9]{64}$')) {
            throw 'Invalid recovery ownership hash'
        }
    }
    if (-not $Journal.ownership_after_hash) { throw 'Missing recovery ownership hash' }
    $transactionPath = Assert-Contained $profilePath (Join-Path $statePath ('transactions/' + $Journal.id))
    foreach ($entry in @($Journal.entries)) {
        Assert-ManagedRelative $entry.path
        $target = Assert-Contained $profilePath (Join-Path $configPath $entry.path)
        $current = Get-Hash $target
        if (($current -ne $entry.before_hash) -and ($current -ne $entry.after_hash)) {
            throw "Recovery refuses user drift: $($entry.path)"
        }
        if ($entry.before_hash) {
            $backup = Assert-Contained $profilePath (Join-Path $transactionPath ('backups/' + $entry.path))
            if ((Get-Hash $backup) -ne $entry.before_hash) { throw "Invalid recovery backup: $($entry.path)" }
        }
    }
    $currentOwner = Get-Hash $ownershipPath
    if (($currentOwner -ne $Journal.ownership_before_hash) -and ($currentOwner -ne $Journal.ownership_after_hash)) {
        throw 'Recovery refuses ownership-state drift'
    }
    if ($Journal.ownership_before_hash) {
        $ownerBackup = Assert-Contained $profilePath (Join-Path $transactionPath 'ownership.before.json')
        if ((Get-Hash $ownerBackup) -ne $Journal.ownership_before_hash) { throw 'Invalid ownership backup' }
    }
}

function Restore-Journal($Journal) {
    Assert-Recoverable $Journal
    $transactionPath = Assert-Contained $profilePath (Join-Path $statePath ('transactions/' + $Journal.id))
    $ownerBackup = Assert-Contained $profilePath (Join-Path $transactionPath 'ownership.before.json')
    foreach ($entry in @($Journal.entries)) {
        $target = Assert-Contained $profilePath (Join-Path $configPath $entry.path)
        $current = Get-Hash $target
        if ($current -eq $entry.before_hash) { continue }
        if ($current -ne $entry.after_hash) { throw "Recovery refuses user drift: $($entry.path)" }
        if ($entry.before_hash) {
            $backup = Assert-Contained $profilePath (Join-Path $transactionPath ('backups/' + $entry.path))
            $restore = Assert-Contained $profilePath (Join-Path $transactionPath ('restore/' + $entry.path))
            Ensure-Directory ([IO.Path]::GetDirectoryName($restore))
            if ((Get-Hash $backup) -ne $entry.before_hash) { throw "Recovery backup changed: $($entry.path)" }
            $null = Assert-Contained $profilePath $restore
            [IO.File]::Copy($backup, $restore, $true)
            if ((Get-Hash $restore) -ne $entry.before_hash) { throw "Recovery restore bytes changed: $($entry.path)" }
            if ((Get-Hash $target) -ne $current) { throw "Recovery refuses concurrent user drift: $($entry.path)" }
            Put-File $restore $target
        } else {
            if ((Get-Hash $target) -ne $current) { throw "Recovery refuses concurrent user drift: $($entry.path)" }
            [IO.File]::Delete($target)
        }
    }
    $currentOwner = Get-Hash $ownershipPath
    if (($currentOwner -ne $Journal.ownership_before_hash) -and ($currentOwner -ne $Journal.ownership_after_hash)) {
        throw 'Recovery refuses ownership-state drift'
    }
    if ($currentOwner -ne $Journal.ownership_before_hash) {
        if ($Journal.ownership_before_hash) {
            $restore = Assert-Contained $profilePath (Join-Path $transactionPath 'ownership.restore.json')
            if ((Get-Hash $ownerBackup) -ne $Journal.ownership_before_hash) { throw 'Recovery ownership backup changed' }
            [IO.File]::Copy($ownerBackup, $restore, $true)
            if ((Get-Hash $restore) -ne $Journal.ownership_before_hash) { throw 'Recovery ownership restore bytes changed' }
            if ((Get-Hash $ownershipPath) -ne $currentOwner) { throw 'Recovery refuses concurrent ownership-state drift' }
            Put-File $restore $ownershipPath
        } else {
            if ((Get-Hash $ownershipPath) -ne $currentOwner) { throw 'Recovery refuses concurrent ownership-state drift' }
            [IO.File]::Delete($ownershipPath)
        }
    }
    $Journal.status = 'rolled_back'
    Write-Json $journalPath $Journal
}

$lockHandle = $null
$activeJournal = $null
try {
    if ([string]::IsNullOrWhiteSpace($ProfileRoot)) { throw 'ProfileRoot is required' }
    if ($Uninstall -and $Recover) { throw '-Uninstall and -Recover are separate operations' }
    $profilePath = [IO.Path]::GetFullPath($ProfileRoot)
    if ($env:GOBAL_INSTALL_TEST_FAIL_AFTER -or $env:GOBAL_INSTALL_TEST_INTERRUPT_AFTER -or $env:GOBAL_INSTALL_TEST_INTERRUPT_BEFORE_COMMIT) {
        $null = Assert-Contained ([IO.Path]::GetTempPath()) $profilePath
        if ($profilePath -eq [IO.Path]::GetFullPath($env:USERPROFILE)) { throw 'Fault injection is forbidden on the real profile' }
    }
    Assert-NoReparseAncestors $profilePath
    $configPath = Assert-Contained $profilePath (Join-Path $profilePath '.gemini/config')
    $statePath = Assert-Contained $profilePath (Join-Path $configPath '.gobal-agent-skills')
    $ownershipPath = Assert-Contained $profilePath (Join-Path $statePath 'pilot-ownership.json')
    $journalPath = Assert-Contained $profilePath (Join-Path $statePath 'pilot-journal.json')
    $payload = [ordered]@{}
    if (-not $Uninstall -and -not $Recover) {
        $pilotSource = [IO.Path]::GetFullPath((Join-Path $SourcePath 'pilot'))
        Assert-NoReparseAncestors $pilotSource
        $payload = Read-Payload $pilotSource
    }
    foreach ($relative in $payload.Keys) { $null = Assert-Contained $profilePath (Join-Path $configPath $relative) }
    Write-Warning 'The temporary pilot always_on rule affects other chats while installed. Remove it promptly after scoring.'
    if ($DryRun) {
        if (Test-Path -LiteralPath $journalPath) {
            $pending = Read-Json $journalPath
            if ($pending.status -eq 'applying' -and -not $Recover) {
                throw 'Pending journal requires -Recover before planning another operation'
            }
        }
        if ($Recover) {
            if (Test-Path -LiteralPath $journalPath) {
                $pending = Read-Json $journalPath
                if ($pending.status -eq 'applying') { Assert-Recoverable $pending }
            }
            Write-Output 'DRY RUN: checked pending recovery; no writes.'
            exit 0
        }
        $owned = Read-Ownership
        $null = Get-Operations $owned $payload
        Write-Output "DRY RUN: validated $($payload.Count) pilot files; no writes."
        exit 0
    }
    Ensure-Directory $statePath
    $lockPath = Assert-Contained $profilePath (Join-Path $statePath 'pilot.lock')
    try { $lockHandle = [IO.File]::Open($lockPath, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None) }
    catch { throw 'Another pilot installer holds the exclusive lock' }
    if (Test-Path -LiteralPath $journalPath) {
        $pending = Read-Json $journalPath
        if ($pending.status -eq 'applying') {
            if ($Recover) {
                Restore-Journal $pending
                Write-Output 'Pilot recovery completed; previous managed bytes and ownership restored.'
                exit 0
            }
            throw 'Pending journal requires -Recover before installing'
        }
    }
    if ($Recover) { Write-Output 'No pending pilot transaction to recover.'; exit 0 }
    $owned = Read-Ownership
    $operations = Get-Operations $owned $payload
    $ownershipUnchanged = $owned.Count -eq $payload.Count
    foreach ($relative in $payload.Keys) {
        if (-not $owned.Contains($relative) -or $owned[$relative] -ne $payload[$relative]) {
            $ownershipUnchanged = $false
            break
        }
    }
    if ($operations.Count -eq 0 -and $ownershipUnchanged) {
        Write-Output 'Pilot no-op; 0 managed file operations. Ownership is unchanged; no transaction or staging created.'
        Write-Output 'Reload Antigravity and independently verify pilot discovery and activation; remove the pilot after scoring.'
        exit 0
    }
    $transactionId = [guid]::NewGuid().ToString('D')
    $transactionPath = Assert-Contained $profilePath (Join-Path $statePath ('transactions/' + $transactionId))
    Ensure-Directory $transactionPath
    # Fully stage the validated source payload before the first managed write.
    foreach ($relative in $payload.Keys) {
        $staged = Assert-Contained $profilePath (Join-Path $transactionPath ('stage/' + $relative))
        Ensure-Directory ([IO.Path]::GetDirectoryName($staged))
        $sourceFile = Assert-Contained $pilotSource (Join-Path $pilotSource $relative)
        [IO.File]::Copy($sourceFile, $staged, $false)
        if ((Get-Hash $staged) -ne $payload[$relative]) { throw 'Source changed while staging' }
    }
    foreach ($entry in $operations) {
        if ($entry.before_hash) {
            $target = Join-Path $configPath $entry.path
            $backup = Assert-Contained $profilePath (Join-Path $transactionPath ('backups/' + $entry.path))
            Ensure-Directory ([IO.Path]::GetDirectoryName($backup))
            [IO.File]::Copy($target, $backup, $false)
            if ((Get-Hash $backup) -ne $entry.before_hash) { throw 'Destination changed while backing up' }
        }
    }
    $ownerBeforeHash = Get-Hash $ownershipPath
    if ($ownerBeforeHash) { [IO.File]::Copy($ownershipPath, (Join-Path $transactionPath 'ownership.before.json'), $false) }
    $ownerAfter = Join-Path $transactionPath 'ownership.after.json'
    Write-Json $ownerAfter ([ordered]@{ schema_version = 1; scope = 'pilot'; files = $payload })
    $activeJournal = [ordered]@{
        schema_version = 1; scope = 'pilot'; id = $transactionId; status = 'applying'
        entries = @($operations); ownership_before_hash = $ownerBeforeHash
        ownership_after_hash = (Get-Hash $ownerAfter)
    }
    Write-Json $journalPath $activeJournal
    $operationCount = 0
    foreach ($entry in $operations) {
        $target = Assert-Contained $profilePath (Join-Path $configPath $entry.path)
        if ($entry.after_hash) {
            $staged = Assert-Contained $profilePath (Join-Path $transactionPath ('stage/' + $entry.path))
            if ((Get-Hash $staged) -ne $entry.after_hash) { throw "Staged payload changed before write: $($entry.path)" }
            if ((Get-Hash $target) -ne $entry.before_hash) { throw "Destination changed before write: $($entry.path)" }
            Put-File $staged $target
        } else {
            if ((Get-Hash $target) -ne $entry.before_hash) { throw "Destination changed before write: $($entry.path)" }
            [IO.File]::Delete($target)
        }
        $operationCount += 1
        Invoke-TestFault $operationCount
    }
    if ((Get-Hash $ownerAfter) -ne $activeJournal.ownership_after_hash) { throw 'Staged ownership changed before commit' }
    if ((Get-Hash $ownershipPath) -ne $activeJournal.ownership_before_hash) { throw 'Ownership changed before commit' }
    Put-File $ownerAfter $ownershipPath
    if ($env:GOBAL_INSTALL_TEST_INTERRUPT_BEFORE_COMMIT -eq '1') { [Environment]::Exit(97) }
    $activeJournal.status = 'committed'
    try { Write-Json $journalPath $activeJournal }
    catch { $activeJournal.status = 'applying'; throw }
    $verb = 'installed'
    if ($Uninstall) { $verb = 'uninstalled' }
    Write-Output "Pilot $verb; $($operations.Count) managed file operations. Backup: $transactionPath"
    Write-Output 'Reload Antigravity and independently verify pilot discovery and activation; remove the pilot after scoring.'
    exit 0
} catch {
    if ($activeJournal -and $activeJournal.status -eq 'applying') {
        try { Restore-Journal $activeJournal }
        catch { Write-Warning "Rollback needs explicit recovery: $_" }
    }
    Write-Error $_ -ErrorAction Continue
    exit 1
} finally {
    if ($lockHandle) { $lockHandle.Dispose() }
}
