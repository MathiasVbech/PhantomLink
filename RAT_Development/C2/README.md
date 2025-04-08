# C2/README.md

## Command & Control Server Component
This component handles the creation of steganographic command images for system control.

### Setup Requirements
- Python 3.10+
- Required packages: PIL, numpy

### Usage Guide
1. Prepare Command:
   in the commands.txt write target powershell commands

2. Create Command Image:
   bash
   python hide_command.py TargetImage.png Commands.txt

3. Command Image Upload:
   -Upload the generated commands.png to your Dropbox app 
   -Or copy and paste the picture to the LocalTesting execute_commands folder

### Available Command Templates

1. Command_upload_TXT_to_dropbox.txt: Upload files to Dropbox needs an API key 
2. get_system_info.txt: Gather system information
3. malware_online_pop_up.txt: Display test message
4. malware_live_new_command.txt: Changes messages from nr. 3. to show continuous execution
5. process_information.txt: Get running processes

### File Structure

hide_command.py: Steganography implementation
TargetImage.png: Base image for hiding commands
Commands/: Directory containing command templates