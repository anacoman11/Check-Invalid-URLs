$repoPath = Get-Location
$pythonScript = Join-Path -Path $repoPath -ChildPath "checkInvalidURLs.py"

if (-Not (Test-Path -Path $pythonScript)) {
    Write-Host "Error: Script checkInvalidURLs.py not found in $repoPath." -ForegroundColor Red
    exit 1
}

$OS_TYPE = $env:OS

if ($OS_TYPE -like "*Windows*") {
    $profileFile = Join-Path -Path $HOME -ChildPath "Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"

    if (-Not (Test-Path -Path $profileFile)) {
        Write-Host "The file $profileFile doesn't exist. We create it now..."
        New-Item -ItemType File -Path $profileFile -Force | Out-Null
    }

    $aliasCommand = "function checkInvalidURL { python3 `"$pythonScript`" }"

    if (Get-Content -Path $profileFile | Select-String -Pattern "checkInvalidURL") {
        Write-Host "The checkInvalidURL alias is already added to the $profileFile."
    } else {
        Add-Content -Path $profileFile -Value $aliasCommand
        Write-Host "The Invalid URL check alias has been added in $profileFile."
    }

    Write-Host "To apply the changes, close and reopen PowerShell."
} else {
    Write-Host "Error: The operating system is not supported." -ForegroundColor Red
    exit 1
}

Write-Host "The setup is complete! You can use the 'checkInvalidURL' command from any directory."
