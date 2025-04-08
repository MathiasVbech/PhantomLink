# hide_command.py
from PIL import Image
import numpy as np
import os
import sys

def hide_text_in_image(image_path, output_path, text):
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        data = np.array(img)

        # Convert text to binary, with length prefix
        text_length = len(text)
        length_binary = format(text_length, '016b')  # 16 bits for length
        text_binary = ''.join(format(ord(c), '08b') for c in text)
        binary = length_binary + text_binary

        if len(binary) > data.size:
            raise ValueError("Text too large for image")

        # Modify pixels
        data_flat = data.flatten()
        for i in range(len(binary)):
            data_flat[i] = (data_flat[i] & ~1) | int(binary[i])
        
        data_modified = data_flat.reshape(data.shape)
        new_img = Image.fromarray(data_modified)
        new_img.save(output_path, 'PNG')
        return True
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 hide_command.py <input_image.png> <commands.txt>")
        return

    input_image = sys.argv[1]
    commands_file = sys.argv[2]

    if not os.path.exists(input_image):
        print(f"Error: Input image '{input_image}' not found")
        return

    if not input_image.lower().endswith('.png'):
        print("Error: Input image must be a PNG file")
        return

    if not os.path.exists(commands_file):
        print(f"Error: Commands file '{commands_file}' not found")
        return

    with open(commands_file, 'r', encoding='utf-8') as file:
        commands = file.read()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_image = os.path.join(script_dir, 'commands.png')

    if hide_text_in_image(input_image, output_image, commands):
        print("Commands hidden successfully in 'commands.png'")

if __name__ == "__main__":
    main()