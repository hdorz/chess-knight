Write-Host "Starting script for creating Python virtual environment..." -f Green

$WorkingDirectory = Get-Location

Write-Host "Changing directory..." -f Green
Set-Location .\..

Write-Host "Creating Python virtual environment..." -f Green
python3.12 -m venv .venv
Write-Host "Python virtual environment created" -f Green

Write-Host "Activating python environment..." -f Green
.\.venv\Scripts\activate
Write-Host "Activated" -f Green

Set-Location $WorkingDirectory

Write-Host "installing requirements into virtual env..." -f Green
pip install -r requirements.txt



Write-Host "Script closing..." -f Green