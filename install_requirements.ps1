$WorkingDirectory = Get-Location

Write-Host "Changing directory..." -f Green
Set-Location .\..

Write-Host "Activating python environment..." -f Green
.\.venv\Scripts\activate
Write-Host "Activated" -f Green

Write-Host "Changing directory back to original directory..." -f Green
Set-Location $WorkingDirectory

Write-Host "Installing requirements into virtual env..." -f Green
pip install -r requirements.txt

Write-Host "Closing script..." -f Green
