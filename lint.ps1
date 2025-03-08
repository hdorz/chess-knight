Write-Host "Starting script for python file linting..." -f Green

$WorkingDirectory = Get-Location


Write-Host "Activating python environment..." -f Green
.\..\.venv\Scripts\activate

Write-Host "Changing directory..." -f Green
Set-Location .\src

Write-Host "Running black..." -f Green
black .\
Write-Host "Black done." -f Green

Write-Host "Running isort..." -f Green
Write-Host "Showing isort filtered output..." -f Green
isort --profile black . --check-only -v | Select-String ".*C:.*|.*(S|s)kipped.*"
Write-Host "isort working on files..." -f Green
isort --profile black .
Write-Host "isort done." -f Green


Set-Location $WorkingDirectory

Write-Host "Script closing..." -f Green

