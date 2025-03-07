# Script to resize assets to 100x100 (assuming they are already square)

$WorkingDirectory = Get-Location

$directory = $args[0]
Set-Location $directory

$Files = Get-ChildItem
$FilesLength = $Files.Length

for (($i = 0); $i -lt $FilesLength; $i++)
{
    $outputName = "={0}" -f $Files[$i]
    ffmpeg -i $Files[$i] -vf scale="100:-1" $outputName
    Remove-Item $Files[$i]
}

Get-ChildItem =*.png | Rename-Item -NewName {$_.Name -replace '=', ''}

Set-Location $WorkingDirectory
