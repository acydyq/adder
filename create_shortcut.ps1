# PowerShell script to create a clickable .exe shortcut for Keep Awake Utility

# Get the base directory where the script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Define the batch file path
$BatchFilePath = Join-Path $ScriptDir "start_keep_awake.bat"

# Define the shortcut file path
$ShortcutPath = Join-Path $ScriptDir "KeepAwake.exe.lnk"

# Define the icon file path
$IconPath = Join-Path $ScriptDir "generated-icon.png"

# Create a WScript Shell object
$WshShell = New-Object -ComObject WScript.Shell

# Create a shortcut
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $BatchFilePath
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.WindowStyle = 1  # Normal window
$Shortcut.Description = "Keep Awake Utility - Prevents your PC from sleeping"
$Shortcut.IconLocation = $IconPath
$Shortcut.Save()

Write-Host "Shortcut created successfully at: $ShortcutPath"
Write-Host "You can now double-click the shortcut to run the Keep Awake Utility."