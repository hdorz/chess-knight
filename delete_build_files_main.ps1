function DeleteItem {
    param (
        $ItemName
    )

    If (Test-Path $ItemName) {
        Remove-Item -Path $ItemName -Recurse
        Write-Host "$ItemName deleted" -f Green
    }
    Else {
        Write-Host "$ItemName does not exist! Already deleted." -f Red
    }

}

Write-Host "Starting script for deleting build file artefacts..." -f Green

$WorkingDirectory = Get-Location
Write-Host "Changing directory..." -f Green
Set-Location .\src

Write-Host "Deleting build folder..." -f Green
DeleteItem -ItemName .\build

Write-Host "Deleting dist folder..." -f Green
DeleteItem -ItemName .\dist

Write-Host "Deleting main.spec file..." -f Green
DeleteItem -ItemName .\main.spec

Set-Location $WorkingDirectory

Write-Host "Build file artefacts deleted." -f Green
