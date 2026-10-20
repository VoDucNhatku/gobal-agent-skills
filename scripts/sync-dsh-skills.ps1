# Mirrors the installed Claude skills into DeepSeek Harness (dsh), hidden from the model catalog
# so they cost no tokens until called with /name. Re-run after install_v2.mjs or after editing
# skills in ~/.claude/skills. The source skills are never modified.
#
# Two mirrors are kept, one per agent preset:
#   <Lab>\home\skills        -> "Standard" preset: every skill hidden (slash-only, cheapest)
#   <Lab>\home\skills-admin  -> "Admin" preset:    every skill visible (skills can call each other)
# Run without -Target to rebuild both:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\sync-dsh-skills.ps1 [-Lab C:\dsh-lab]
param(
    [string]$Target,
    # Skills listed here stay visible to the model (auto-invocable); everything else is slash-command only.
    [string[]]$ModelVisible = @(),
    [switch]$AllVisible,
    [string]$Source = (Join-Path $HOME '.claude\skills'),
    [string]$Lab = 'C:\dsh-lab'
)

$ErrorActionPreference = 'Stop'
# dsh-only skills (e.g. read-docx-full) live here; they are mirrored into both presets and stay model-visible.
$extraSource = Join-Path $Lab 'dsh-skills'
$alwaysVisible = @('read-docx-full')

if (-not (Test-Path (Join-Path $Source '_shared'))) {
    throw "No v2 install at $Source (missing _shared). Run node scripts/install_v2.mjs first."
}
if (-not $Target) {
    & $PSCommandPath -Target (Join-Path $Lab 'home\skills') -ModelVisible $ModelVisible -Source $Source -Lab $Lab
    & $PSCommandPath -Target (Join-Path $Lab 'home\skills-admin') -AllVisible -Source $Source -Lab $Lab
    return
}
$target = $Target
$skillDirs = @(Get-ChildItem $Source -Directory) + @(Get-ChildItem $extraSource -Directory -ErrorAction SilentlyContinue)
if ($AllVisible) { $ModelVisible = $skillDirs.Name }
$ModelVisible = @($ModelVisible) + $alwaysVisible

# Clean up the previous mirror WITHOUT recursing through junctions (Remove-Item -Recurse on
# Windows PowerShell 5.1 can follow a junction and delete the original skill files).
function Remove-Mirror([string]$path) {
    $item = Get-Item -LiteralPath $path -Force
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { $item.Delete(); return }  # unlink only
    foreach ($child in Get-ChildItem -LiteralPath $path -Force) {
        if ($child.PSIsContainer) { Remove-Mirror $child.FullName } else { $child.Delete() }
    }
    $item.Delete()
}
if (Test-Path $target) { Remove-Mirror $target }
New-Item -ItemType Directory $target | Out-Null

# v2 skills read shared rules via ../_shared/...; link it so those relative paths resolve in the mirror.
New-Item -ItemType Junction -Path (Join-Path $target '_shared') -Target (Join-Path $Source '_shared') | Out-Null

$count = 0
foreach ($dir in $skillDirs) {
    $skillFile = Join-Path $dir.FullName 'SKILL.md'
    if (-not (Test-Path $skillFile)) { continue }

    $dest = Join-Path $target $dir.Name
    New-Item -ItemType Directory $dest | Out-Null

    # Subfolders (references, scripts, resources...) point back to the original so relative paths keep working.
    foreach ($sub in Get-ChildItem $dir.FullName -Directory) {
        New-Item -ItemType Junction -Path (Join-Path $dest $sub.Name) -Target $sub.FullName | Out-Null
    }
    # Other top-level files are copied as-is.
    Get-ChildItem $dir.FullName -File | Where-Object Name -ne 'SKILL.md' | Copy-Item -Destination $dest

    # Read and write as UTF-8 explicitly: Get-Content on Windows PowerShell 5.1 decodes BOM-less
    # UTF-8 as ANSI, which garbles Vietnamese text when written back.
    $text = [IO.File]::ReadAllText($skillFile, [Text.Encoding]::UTF8)
    if ($ModelVisible -notcontains $dir.Name -and $text -match '^---\r?\n') {
        $text = [regex]::Replace($text, '(?m)\A(---\r?\n(?:(?!---).*\r?\n)*?)disable-model-invocation:.*\r?\n', '$1')
        $text = [regex]::Replace($text, '\A---(\r?\n)', '---$1disable-model-invocation: true$1')
    }
    [IO.File]::WriteAllText((Join-Path $dest 'SKILL.md'), $text, (New-Object Text.UTF8Encoding $false))
    $count++
}
$visible = if ($AllVisible) { 'all' } elseif ($ModelVisible) { $ModelVisible -join ', ' } else { 'none' }
"synced $count skills into $target; model-visible: $visible"
