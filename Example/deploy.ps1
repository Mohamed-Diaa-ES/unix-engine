# --- CONFIGURATION ---
$Url = "http://127.0.0.1:8050/run"
$ProjectName = (Get-Item .).Name  # Grabs the folder name (e.g., "TestProject")
$TempZip = "project.zip"
$OutputApp = "$ProjectName.out"   # Local file will now match project name
$curl = "C:\Windows\System32\curl.exe"

Write-Host "--- Unix Engine: Hyper-V Mode ($ProjectName) ---" -ForegroundColor Cyan

# 1. Packaging
if (Test-Path $TempZip) { Remove-Item $TempZip }
tar.exe -a -c -f $TempZip --exclude=".vscode" --exclude=".git" --exclude=$TempZip --exclude="deploy.ps1" --exclude="*.out" *

# 2. Shipping (Now sending project_name as a field)
Write-Host "Action: Sending to Factory..."
$statusCode = (& $curl -s -w "%{http_code}" -o $OutputApp -X POST -F "file=@$TempZip" -F "project_name=$ProjectName" $Url).Trim()

# 3. Cleanup & Results
if (Test-Path $TempZip) { Remove-Item $TempZip }
if ($statusCode -eq "200") {
    Write-Host " Success! Received: $OutputApp" -ForegroundColor Green
} else {
    Write-Host "Error $statusCode" -ForegroundColor Red
    if (Test-Path $OutputApp) { Get-Content $OutputApp; Remove-Item $OutputApp }
}