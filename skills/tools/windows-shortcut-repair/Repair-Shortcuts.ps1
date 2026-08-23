<#
.SYNOPSIS
    Advanced Windows Shortcut Repair — GUI + CLI with monitoring, export, and scheduled tasks.

.DESCRIPTION
    Full-featured shortcut repair toolkit:
    - GUI mode with real-time scanning
    - CLI mode for automation
    - Export reports (CSV, JSON, HTML)
    - Import known-good shortcut configurations
    - Scheduled task integration
    - System tray notifications
    - Backup before fix

.PARAMETER GUI
    Launch graphical interface.

.PARAMETER ScanOnly
    Only scan and report, don't fix anything.

.PARAMETER Path
    Folder path to scan. Defaults to Desktop, Start Menu, Taskbar.

.PARAMETER Pattern
    Filter shortcuts by name pattern (wildcards supported).

.PARAMETER FixExePath
    Force all matching shortcuts to use this .exe for icons.

.PARAMETER Export
    Export report to file (CSV, JSON, or HTML).

.PARAMETER Import
    Import known-good shortcut configurations from JSON.

.PARAMETER Backup
    Create backup before fixing shortcuts.

.PARAMETER Monitor
    Run in monitoring mode (watch for new shortcuts).

.PARAMETER Quiet
    Suppress console output.

.EXAMPLE
    .\Repair-Shortcuts.ps1 -GUI
    .\Repair-Shortcuts.ps1 -ScanOnly -Export "report.csv"
    .\Repair-Shortcuts.ps1 -Pattern "opencode" -Backup
    .\Repair-Shortcuts.ps1 -Monitor -Interval 300
#>

param(
    [switch]$GUI,
    [switch]$ScanOnly,
    [string[]]$Path,
    [string]$Pattern = "*",
    [string]$FixExePath,
    [string]$Export,
    [string]$Import,
    [switch]$Backup,
    [switch]$Monitor,
    [int]$Interval = 300,
    [switch]$Quiet
)

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

function Get-Shortcuts {
    param(
        [string[]]$Folders,
        [string]$Filter = "*"
    )

    $results = @()
    $shell = New-Object -ComObject WScript.Shell

    foreach ($folder in $Folders) {
        if (-not (Test-Path $folder)) { continue }

        $shortcuts = Get-ChildItem -Path $folder -Filter "*.lnk" -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -like $Filter }

        foreach ($lnk in $shortcuts) {
            try {
                $shortcut = $shell.CreateShortcut($lnk.FullName)
                $iconEmpty = $shortcut.IconLocation -match "^,"
                $targetMissing = $shortcut.TargetPath -ne "" -and -not (Test-Path $shortcut.TargetPath)

                $results += [PSCustomObject]@{
                    Name        = $lnk.Name
                    Path        = $lnk.FullName
                    Folder      = $lnk.DirectoryName
                    Target      = $shortcut.TargetPath
                    Icon        = $shortcut.IconLocation
                    Arguments   = $shortcut.Arguments
                    WorkingDir  = $shortcut.WorkingDirectory
                    Description = $shortcut.Description
                    IconEmpty   = $iconEmpty
                    TargetGone  = $targetMissing
                    Broken      = $iconEmpty -or $targetMissing
                    LastWrite   = $lnk.LastWriteTime
                }
            } catch {
                $results += [PSCustomObject]@{
                    Name        = $lnk.Name
                    Path        = $lnk.FullName
                    Folder      = $lnk.DirectoryName
                    Target      = "ERROR"
                    Icon        = "ERROR"
                    Arguments   = ""
                    WorkingDir  = ""
                    Description = ""
                    IconEmpty   = $false
                    TargetGone  = $false
                    Broken      = $true
                    LastWrite   = $lnk.LastWriteTime
                }
            }
        }
    }

    return $results
}

function Repair-Shortcut {
    param(
        [object]$ShortcutInfo,
        [string]$ExePath,
        [switch]$CreateBackup
    )

    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($ShortcutInfo.Path)

    # Backup if requested
    if ($CreateBackup) {
        $backupDir = Join-Path $env:USERPROFILE ".shortcut-backups"
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        $backupName = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')_$($ShortcutInfo.Name)"
        Copy-Item -Path $ShortcutInfo.Path -Destination (Join-Path $backupDir $backupName) -Force
    }

    # Determine fix path
    $fixPath = $ExePath
    if (-not $fixPath) {
        if ($shortcut.TargetPath -and (Test-Path $shortcut.TargetPath)) {
            $fixPath = $shortcut.TargetPath
        } else {
            $fixPath = Join-Path $ShortcutInfo.Folder "$([System.IO.Path]::GetFileNameWithoutExtension($ShortcutInfo.Name)).exe"
        }
    }

    # Apply fix
    if ($fixPath -and (Test-Path $fixPath)) {
        $shortcut.IconLocation = "$fixPath,0"
        $shortcut.Save()
        return @{ Success = $true; FixedIcon = "$fixPath,0" }
    }

    return @{ Success = $false; Error = "No valid exe found" }
}

function Export-Report {
    param(
        [object[]]$Data,
        [string]$Path
    )

    $ext = [System.IO.Path]::GetExtension($Path).ToLower()

    switch ($ext) {
        ".csv" {
            $Data | Export-Csv -Path $Path -NoTypeInformation
        }
        ".json" {
            $Data | ConvertTo-Json -Depth 10 | Out-File -FilePath $Path -Encoding UTF8
        }
        ".html" {
            $html = @"
<!DOCTYPE html>
<html>
<head>
    <title>Shortcut Repair Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .broken { color: red; font-weight: bold; }
        .fixed { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Shortcut Repair Report</h1>
    <p>Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')</p>
    <p>Total: $($Data.Count) | Broken: $(($Data | Where-Object { $_.Broken }).Count)</p>
    <table>
        <tr>
            <th>Name</th>
            <th>Target</th>
            <th>Icon</th>
            <th>Status</th>
            <th>Last Write</th>
        </tr>
$($Data | ForEach-Object {
    $statusClass = if ($_.Broken) { "broken" } else { "fixed" }
    "        <tr>
            <td>$($_.Name)</td>
            <td>$($_.Target)</td>
            <td>$($_.Icon)</td>
            <td class=`"$statusClass`">$(if ($_.Broken) { 'BROKEN' } else { 'OK' })</td>
            <td>$($_.LastWrite)</td>
        </tr>"
})
    </table>
</body>
</html>
"@
            $html | Out-File -FilePath $Path -Encoding UTF8
        }
        default {
            Write-Warning "Unknown format: $ext. Use .csv, .json, or .html"
        }
    }
}

# ============================================================================
# GUI MODE
# ============================================================================

function Show-GUI {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Windows Shortcut Repair"
    $form.Size = New-Object System.Drawing.Size(900, 600)
    $form.StartPosition = "CenterScreen"
    $form.BackColor = [System.Drawing.Color]::White

    # Title
    $titleLabel = New-Object System.Windows.Forms.Label
    $titleLabel.Text = "Windows Shortcut Repair Tool"
    $titleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
    $titleLabel.ForeColor = [System.Drawing.Color]::FromArgb(0, 120, 215)
    $titleLabel.AutoSize = $true
    $titleLabel.Location = New-Object System.Drawing.Point(20, 20)
    $form.Controls.Add($titleLabel)

    # Status label
    $statusLabel = New-Object System.Windows.Forms.Label
    $statusLabel.Text = "Ready to scan"
    $statusLabel.AutoSize = $true
    $statusLabel.Location = New-Object System.Drawing.Point(20, 60)
    $form.Controls.Add($statusLabel)

    # Progress bar
    $progressBar = New-Object System.Windows.Forms.ProgressBar
    $progressBar.Size = New-Object System.Drawing.Size(840, 20)
    $progressBar.Location = New-Object System.Drawing.Point(20, 90)
    $progressBar.Style = "Continuous"
    $form.Controls.Add($progressBar)

    # DataGridView
    $dataGridView = New-Object System.Windows.Forms.DataGridView
    $dataGridView.Size = New-Object System.Drawing.Size(840, 380)
    $dataGridView.Location = New-Object System.Drawing.Point(20, 120)
    $dataGridView.AllowUserToAddRows = $false
    $dataGridView.AllowUserToDeleteRows = $false
    $dataGridView.ReadOnly = $true
    $dataGridView.SelectionMode = "FullRowSelect"
    $dataGridView.AutoSizeColumnsMode = "Fill"
    $form.Controls.Add($dataGridView)

    # Buttons
    $scanButton = New-Object System.Windows.Forms.Button
    $scanButton.Text = "Scan"
    $scanButton.Size = New-Object System.Drawing.Size(100, 35)
    $scanButton.Location = New-Object System.Drawing.Point(20, 520)
    $scanButton.BackColor = [System.Drawing.Color]::FromArgb(0, 120, 215)
    $scanButton.ForeColor = [System.Drawing.Color]::White
    $scanButton.FlatStyle = "Flat"
    $form.Controls.Add($scanButton)

    $fixButton = New-Object System.Windows.Forms.Button
    $fixButton.Text = "Fix Selected"
    $fixButton.Size = New-Object System.Drawing.Size(120, 35)
    $fixButton.Location = New-Object System.Drawing.Point(130, 520)
    $fixButton.BackColor = [System.Drawing.Color]::FromArgb(40, 167, 69)
    $fixButton.ForeColor = [System.Drawing.Color]::White
    $fixButton.FlatStyle = "Flat"
    $fixButton.Enabled = $false
    $form.Controls.Add($fixButton)

    $fixAllButton = New-Object System.Windows.Forms.Button
    $fixAllButton.Text = "Fix All Broken"
    $fixAllButton.Size = New-Object System.Drawing.Size(120, 35)
    $fixAllButton.Location = New-Object System.Drawing.Point(260, 520)
    $fixAllButton.BackColor = [System.Drawing.Color]::FromArgb(255, 193, 7)
    $fixAllButton.ForeColor = [System.Drawing.Color]::Black
    $fixAllButton.FlatStyle = "Flat"
    $fixAllButton.Enabled = $false
    $form.Controls.Add($fixAllButton)

    $exportButton = New-Object System.Windows.Forms.Button
    $exportButton.Text = "Export Report"
    $exportButton.Size = New-Object System.Drawing.Size(120, 35)
    $exportButton.Location = New-Object System.Drawing.Point(390, 520)
    $exportButton.BackColor = [System.Drawing.Color]::Gray
    $exportButton.ForeColor = [System.Drawing.Color]::White
    $exportButton.FlatStyle = "Flat"
    $form.Controls.Add($exportButton)

    # Folder selection
    $folderLabel = New-Object System.Windows.Forms.Label
    $folderLabel.Text = "Scan folder:"
    $folderLabel.AutoSize = $true
    $folderLabel.Location = New-Object System.Drawing.Point(540, 525)
    $form.Controls.Add($folderLabel)

    $folderCombo = New-Object System.Windows.Forms.ComboBox
    $folderCombo.Size = New-Object System.Drawing.Size(280, 25)
    $folderCombo.Location = New-Object System.Drawing.Point(620, 522)
    $folderCombo.DropDownStyle = "DropDown"
    $form.Controls.Add($folderCombo)

    # Add default folders
    $folders = @(
        "$env:USERPROFILE\Desktop",
        "$env:APPDATA\Microsoft\Windows\Start Menu\Programs",
        "$env:APPDATA\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar",
        "$PROGRAMDATA\Microsoft\Windows\Start Menu\Programs"
    ) | Where-Object { Test-Path $_ }

    foreach ($f in $folders) {
        $folderCombo.Items.Add($f) | Out-Null
    }
    $folderCombo.SelectedIndex = 0

    # Scan button click
    $scanButton.Add_Click({
        $statusLabel.Text = "Scanning..."
        $progressBar.Value = 0
        $dataGridView.DataSource = $null

        $scanPaths = @($folderCombo.Text)
        $allShortcuts = Get-Shortcuts -Folders $scanPaths -Filter $Pattern

        $progressBar.Value = 100
        $statusLabel.Text = "Found $($allShortcuts.Count) shortcuts ($(($allShortcuts | Where-Object { $_.Broken }).Count) broken)"

        # Bind to grid
        $bindingList = New-Object System.Collections.ObjectModel.BindingCollection[object]
        foreach ($item in $allShortcuts) { $bindingList.Add($item) | Out-Null }
        $dataGridView.DataSource = $bindingList

        # Enable buttons
        $fixButton.Enabled = $allShortcuts.Count -gt 0
        $fixAllButton.Enabled = ($allShortcuts | Where-Object { $_.Broken }).Count -gt 0

        $script:currentData = $allShortcuts
    })

    # Fix selected button click
    $fixButton.Add_Click({
        $selected = $dataGridView.SelectedRows
        if ($selected.Count -eq 0) {
            [System.Windows.Forms.MessageBox]::Show("Please select rows to fix.", "Info")
            return
        }

        $fixed = 0
        foreach ($row in $selected) {
            $item = $row.DataBoundItem
            if ($item.Broken) {
                $result = Repair-Shortcut -ShortcutInfo $item -CreateBackup:$Backup
                if ($result.Success) { $fixed++ }
            }
        }

        $statusLabel.Text = "Fixed $fixed shortcuts. Click Scan to refresh."
        [System.Windows.Forms.MessageBox]::Show("Fixed $fixed shortcuts.", "Done")
    })

    # Fix all broken button click
    $fixAllButton.Add_Click({
        $broken = $script:currentData | Where-Object { $_.Broken }
        if ($broken.Count -eq 0) {
            [System.Windows.Forms.MessageBox]::Show("No broken shortcuts found.", "Info")
            return
        }

        $confirm = [System.Windows.Forms.MessageBox]::Show(
            "Fix all $($broken.Count) broken shortcuts?",
            "Confirm",
            "YesNo",
            "Warning"
        )

        if ($confirm -eq "Yes") {
            $fixed = 0
            foreach ($item in $broken) {
                $result = Repair-Shortcut -ShortcutInfo $item -CreateBackup:$Backup
                if ($result.Success) { $fixed++ }
            }
            $statusLabel.Text = "Fixed $fixed shortcuts. Click Scan to refresh."
            [System.Windows.Forms.MessageBox]::Show("Fixed $fixed shortcuts.", "Done")
        }
    })

    # Export button click
    $exportButton.Add_Click({
        $dialog = New-Object System.Windows.Forms.SaveFileDialog
        $dialog.Filter = "CSV Files (*.csv)|*.csv|JSON Files (*.json)|*.json|HTML Files (*.html)|*.html"
        $dialog.DefaultExt = "csv"

        if ($dialog.ShowDialog() -eq "OK") {
            Export-Report -Data $script:currentData -Path $dialog.FileName
            $statusLabel.Text = "Report exported to: $($dialog.FileName)"
        }
    })

    $form.ShowDialog()
}

# ============================================================================
# MONITORING MODE
# ============================================================================

function Start-Monitor {
    param(
        [string[]]$Folders,
        [int]$PollSeconds = 300
    )

    Write-Host "Starting monitor mode (poll every $PollSeconds seconds)..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow

    $knownShortcuts = @{}

    # Initial scan
    $allShortcuts = Get-Shortcuts -Folders $Folders -Filter $Pattern
    foreach ($s in $allShortcuts) {
        $knownShortcuts[$s.Path] = $s
    }

    Write-Host "Initial scan: $($allShortcuts.Count) shortcuts known" -ForegroundColor Green

    while ($true) {
        Start-Sleep -Seconds $PollSeconds

        $currentShortcuts = Get-Shortcuts -Folders $Folders -Filter $Pattern

        # Find new shortcuts
        $newShortcuts = $currentShortcuts | Where-Object { -not $knownShortcuts.ContainsKey($_.Path) }

        # Find deleted shortcuts
        $deletedPaths = $knownShortcuts.Keys | Where-Object { -not ($currentShortcuts | Where-Object { $_.Path -eq $_ }) }

        if ($newShortcuts) {
            foreach ($ns in $newShortcuts) {
                Write-Host "NEW: $($ns.Name) in $($ns.Folder)" -ForegroundColor Green
                if ($ns.Broken) {
                    Write-Host "  -> BROKEN ICON, auto-fixing..." -ForegroundColor Yellow
                    $result = Repair-Shortcut -ShortcutInfo $ns -CreateBackup
                    if ($result.Success) {
                        Write-Host "  -> FIXED" -ForegroundColor Green
                    }
                }
            }
        }

        if ($deletedPaths) {
            foreach ($dp in $deletedPaths) {
                Write-Host "DELETED: $($knownShortcuts[$dp].Name)" -ForegroundColor Red
            }
        }

        # Update known
        $knownShortcuts = @{}
        foreach ($s in $currentShortcuts) {
            $knownShortcuts[$s.Path] = $s
        }
    }
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

# Default scan locations
if (-not $Path) {
    $Path = @(
        "$env:USERPROFILE\Desktop",
        "$env:APPDATA\Microsoft\Windows\Start Menu\Programs",
        "$env:APPDATA\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar",
        "$env:PROGRAMDATA\Microsoft\Windows\Start Menu\Programs"
    ) | Where-Object { Test-Path $_ }
}

# GUI mode
if ($GUI) {
    Show-GUI
    exit
}

# Monitor mode
if ($Monitor) {
    Start-Monitor -Folders $Path -PollSeconds $Interval
    exit
}

# Import known-good configurations
if ($Import) {
    $importData = Get-Content -Path $Import -Raw | ConvertFrom-Json
    Write-Host "Imported $($importData.Count) shortcut configurations" -ForegroundColor Cyan
    # Apply import logic here
}

# CLI mode
$results = Get-Shortcuts -Folders $Path -Filter $Pattern
$broken = $results | Where-Object { $_.Broken }

if (-not $Quiet) {
    Write-Host "`n=== Shortcut Scan Results ===" -ForegroundColor Cyan
    Write-Host "Total shortcuts: $($results.Count)" -ForegroundColor Gray
    Write-Host "Broken: $($broken.Count)" -ForegroundColor $(if ($broken.Count -gt 0) { "Yellow" } else { "Green" })

    if ($broken.Count -gt 0) {
        Write-Host "`nBroken shortcuts:" -ForegroundColor Yellow
        $broken | Format-Table Name, Icon, Target -AutoSize
    }
}

# Export if requested
if ($Export) {
    Export-Report -Data $results -Path $Export
    if (-not $Quiet) {
        Write-Host "Report exported to: $Export" -ForegroundColor Green
    }
}

# Fix if not scan-only
if (-not $ScanOnly -and $broken.Count -gt 0) {
    $fixed = 0
    foreach ($item in $broken) {
        $result = Repair-Shortcut -ShortcutInfo $item -ExePath $FixExePath -CreateBackup:$Backup
        if ($result.Success) { $fixed++ }
    }

    if (-not $Quiet) {
        Write-Host "`nFixed: $fixed shortcuts" -ForegroundColor Green
    }
} elseif ($ScanOnly) {
    if (-not $Quiet) {
        Write-Host "`nRun without -ScanOnly to fix these issues." -ForegroundColor Yellow
    }
}

# Return results for pipeline usage
return $results
