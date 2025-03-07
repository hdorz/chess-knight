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
isort --profile black . --check-only
isort --profile black .
Write-Host "isort done." -f Green


Set-Location $WorkingDirectory

Write-Host "Script closing..." -f Green

