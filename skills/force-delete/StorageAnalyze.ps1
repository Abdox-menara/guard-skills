<#
.SYNOPSIS
Analyse a drive partition – used/free space, largest files, biggest folders.
.DESCRIPTION
Reports drive usage, top N largest files, and size of top‑level folders.
Optionally writes the report to a file.
.PARAMETER Drive
Drive letter to analyse (e.g. "H").
.PARAMETER TopFiles
Number of largest files to show (default 20).
.PARAMETER TopFolders
Number of largest folders to show (default 10).
.PARAMETER OutputFile
Optional path to save the report as a text file.
.EXAMPLE
.\StorageAnalyze.ps1 -Drive H
.\StorageAnalyze.ps1 -Drive D -TopFiles 30 -TopFolders 15 -OutputFile report.txt
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Drive,

    [int]$TopFiles = 20,
    [int]$TopFolders = 10,

    [string]$OutputFile
)

function Write-Report {
    param([string]$Message)
    Write-Host $Message
    if ($OutputFile) {
        Add-Content -Path $OutputFile -Value $Message -Encoding UTF8
    }
}

$driveName = "$Drive`:"
$drv = Get-PSDrive -Name $Drive -ErrorAction SilentlyContinue
if (-not $drv) {
    Write-Report "Drive $driveName not found."
    exit 1
}

$usedGB  = [math]::Round($drv.Used/1GB, 2)
$freeGB  = [math]::Round($drv.Free/1GB, 2)
$totalGB = [math]::Round(($drv.Used+$drv.Free)/1GB, 2)

Write-Report "========================================"
Write-Report "  Storage analysis – $driveName"
Write-Report "========================================"
Write-Report "Used: $usedGB GB | Free: $freeGB GB | Total: $totalGB GB"
Write-Report ""

Write-Report "Top $TopFiles largest files:"
Get-ChildItem -Path "$driveName\" -File -Recurse -ErrorAction SilentlyContinue |
    Sort-Object Length -Descending |
    Select-Object -First $TopFiles |
    ForEach-Object {
        $sizeGB = "{0:N2}" -f ($_.Length / 1GB)
        Write-Report "  $($_.FullName)  $sizeGB GB"
    }

Write-Report ""
Write-Report "Top $TopFolders largest folders:"
Get-ChildItem -Path "$driveName\" -Directory -ErrorAction SilentlyContinue |
    ForEach-Object {
        $size = (Get-ChildItem -Path $_.FullName -Recurse -File -ErrorAction SilentlyContinue |
                  Measure-Object -Property Length -Sum).Sum
        $sizeGB = if ($size) { "{0:N2}" -f ($size / 1GB) } else { "0.00" }
        [pscustomobject]@{ Folder = $_.FullName; SizeGB = [double]$sizeGB }
    } |
    Sort-Object SizeGB -Descending |
    Select-Object -First $TopFolders |
    ForEach-Object {
        Write-Report "  $($_.Folder)  $($_.SizeGB) GB"
    }

if ($OutputFile) {
    Write-Report "Report saved to $OutputFile"
}
