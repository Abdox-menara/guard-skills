<#
.SYNOPSIS
Searches an entire drive (or folder) for directories matching a name pattern,
then forces deletion using takeown + icacls + Remove-Item.
.DESCRIPTION
Useful for cleaning up e.g. old package folders, temp workspaces, or
protected directories whose exact location may vary.
Supports WhatIf, Confirm, logging, and pipeline input for delete action.
.PARAMETER Pattern
Wildcard pattern to match folder names (e.g. "ZZZZZZZZZ", "node_modules", "bin").
.PARAMETER Drive
Root path to search (default D:). Accepts a drive root or a full path.
.PARAMETER TopFiles
If set, shows total size of each matched folder.
.PARAMETER Remove
Switch – actually delete (default is preview-only).
.PARAMETER LogFile
Optional path to write a log of all actions.
.PARAMETER WhatIf
Shows what would happen without making changes.
.PARAMETER Confirm
Prompts for confirmation before each deletion.
.EXAMPLE
.\FindAndDelete.ps1 -Pattern "ZZZZZZZZ" -Drive D
.\FindAndDelete.ps1 -Pattern "ModifiableWindowsApps" -Drive D -Remove -LogFile delete.log
.\FindAndDelete.ps1 -Pattern "cache" -Drive "C:\Users" -TopFiles -Remove -WhatIf
#>

[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
    [Parameter(Mandatory=$true)]
    [string]$Pattern,

    [string]$Drive = "D:",

    [switch]$TopFiles,

    [switch]$Remove,

    [string]$LogFile,

    [switch]$WhatIf
)

function Write-Log {
    param([string]$Message)
    Write-Host $Message
    if ($LogFile) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Add-Content -Path $LogFile -Value "[$timestamp] $Message" -Encoding UTF8
    }
}

# -----------------------------------------------------------------
# Get list of matching directories (force includes hidden/system)
$results = Get-ChildItem -Path $Drive -Recurse -Directory -Force `
            -Filter $Pattern -ErrorAction SilentlyContinue

if (-not $results) {
    Write-Host "No directories matching '$Pattern' found under $Drive" -ForegroundColor Yellow
    exit
}

Write-Log "Found $($results.Count) matched folder(s) for pattern '$Pattern' under $Drive"

if (-not $TopFiles -and -not $Remove) {
    # preview mode
    foreach ($r in $results) {
        Write-Log "  $($r.FullName)"
    }
    Write-Log "Preview mode – add -Remove to actually delete."
    exit
}

foreach ($p in $results) {
    if ($TopFiles) {
        $sz = (Get-ChildItem -Path $p.FullName -Recurse -File -Force -ErrorAction SilentlyContinue |
                Measure-Object -Property Length -Sum).Sum
        Write-Log "$($p.FullName)  $(if($sz){[math]::Round($sz/1MB,2)}else{0}) MB"
    }

    if ($Remove) {
        if ($PSCmdlet.ShouldProcess($p.FullName, "Take ownership, grant control, delete")) {
            Write-Log "Processing $($p.FullName)"
            try {
                & takeown.exe /F $p.FullName /A /R /D Y | Out-Null
                & icacls.exe $p.FullName /grant:r "Administrators:(F)" /T /C | Out-Null
                & attrib -R -S -H $p.FullName /S /D | Out-Null
                Remove-Item -LiteralPath $p.FullName -Recurse -Force -ErrorAction Stop
                Write-Log "  Deleted $($p.FullName)"
            } catch {
                Write-Log "  Failed: $_"
            }
        }
    }
}
