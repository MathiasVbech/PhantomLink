# RAT/LocalTesting/README.md

## Local Testing Environment
Safe testing environment for command execution and keylogging functionality. This folder contains example command images for testing different capabilities.

### Security Note
While this is a local testing environment, always run within a VM for safety.

### Features
Local command execution testing
Multiple test command scenarios
System and process info gathering
Popup message demonstrations
Keylogger capability testing
No network communication
Safe development environment

### Setup
1. Install required packages:
  bash
  pip install pynput pillow numpy

### Folder Structure:
/commands/: Contains test command images
/execute_commands/: Folder watched for command execution
LocalRAT.py: Main testing implementation

### Usage Guide
1: Start the local testing environment:
bash
python LocalRAT.py

2: Testing Commands:
Copy any of the provided command images from /commands/ to /execute_commands/ to test:
Available Test Commands:

Malware_online: Displays popup window saying "Malware online"
Malware_mid_execution_new_command: Shows popup during execution
Print_process_info_to_txt: Saves running process info to file
Print_System_info_to_txt: Saves system information to file

3. Command Testing Process:

Copy desired commands.png from commands subfolder
Paste into execute_commands folder
System will detect, extract and execute commands
Check console output for execution status
Results will be saved to text files for info gathering commands


4. Testing Keylogger:

Keystrokes are logged to keystrokes.txt
No network communication in local testing
View logged keys in the output file

### Test Command Details
Malware Online Test

Location: /commands/Malware_online/
Effect: Creates Windows Form popup
Duration: 5 seconds
Purpose: Basic command execution test

Mid-Execution Command

Location: /commands/Malware_mid_execution_new_command/
Effect: Shows popup during ongoing execution
Purpose: Tests command handling during operations

Process Information

Location: /commands/Print_process_info_to_txt/
Effect: Captures running process details
Output: Saves to text file
Purpose: Tests system info gathering

System Information

Location: /commands/Print_System_info_to_txt/
Effect: Gathers system configuration details
Output: Saves to text file
Purpose: Tests detailed system reconnaissance
