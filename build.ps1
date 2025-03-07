Write-Host "Deleting previous build artefacts..." -f Green
.\delete_build_files_main.ps1

Write-Host "Starting script for building executable of pygame project..." -f Green

$WorkingDirectory = Get-Location

Write-Host "Activating python environment..." -f Green
.\..\.venv\Scripts\activate

Write-Host "Changing directory..." -f Green
Set-Location .\src

Write-Host "Buiding executable..." -f Green
pyinstaller --onefile main.py --collect-data data --noconsole

Write-Host "Updating spec file... (1/2)" -f Green
python $WorkingDirectory\edit_spec_main.py "main.spec" "./chess/data"

Write-Host "Updating spec file... (2/2)" -f Green
pyinstaller main.spec

Write-Host "Renaming executable to 'chess_knight.exe'" -f Green
Set-Location .\dist
Rename-Item -Path ".\main.exe" -NewName "chess_knight.exe"

Set-Location $WorkingDirectory

Write-Host "Script closing..." -f Green
