$sh = New-Object -ComObject WScript.Shell
$lnkPath = 'C:\Users\Public\Desktop\Drive Composer pro 2.9.0.1.lnk'
$lnk = $sh.CreateShortcut($lnkPath)
Write-Host "Target: $($lnk.TargetPath)"
Write-Host "IconLocation: $($lnk.IconLocation)"
Write-Host "WorkingDirectory: $($lnk.WorkingDirectory)"
