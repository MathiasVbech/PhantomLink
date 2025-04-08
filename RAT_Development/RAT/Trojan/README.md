# RAT/Trojan/README.md

## ⚠️ WARNING: MALICIOUS CODE
This component contains potentially harmful code. Only use in controlled VM environments.

### Features
- Steganographic command execution
- Keylogging capability
- Dropbox C2 communication
- System persistence

### Dropbox Setup
1. Create a Dropbox App:
   - Go to https://www.dropbox.com/developers
   - Click "Create app"
   - Choose "Scoped access"
   - Choose "Full Dropbox" access
   - Name your app
   
2. Configure Permissions:
   - Under Permissions tab:
   - Enable files.content.read
   - Enable files.content.write
   
3. Generate Access Token:
   - Go to Settings tab
   - Under "Access token expiration"
   - Choose appropriate time for testing
   - Generate and copy the token

### Installation Guide
1. Prepare Environment:
   - Create folder: Trojan
   - Copy run_commands.py and setup.ps1
   - Or copy the Trojan folder, recommended to place the Trojan folder in the download folder to "simulate" download and installing a trojan program
   - Update DROPBOX_ACCESS_TOKEN in run_commands.py

2. Install Dependencies:
   powershell
   # Run as Administrator
   .\setup.ps1
   -Restart computer after installation

3. Command Usage:
   - Most commands.png will work directly after installation
   For Dropbox upload functionality:
      Create new command image using C2/hide_commands.py
      Use template from C2/Commands/Command_upload_TXT_to_dropbox.txt
      Update API key in template with your Dropbox app key
      Generate new command image with updated credentials

### File Structure
run_commands.py: Main implementation
setup.ps1: Installation script
test.txt: Test file for checking upload commands

⚠️ IMPORTANT: This code can cause harm. Only run in isolated VM environments.