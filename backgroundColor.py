import json
import os
from PIL import Image

# Load the JSON file
with open('rise-of-skulls.json', 'r') as file:
    skulls_data = json.load(file)

# Define the directory paths
images_dir = 'images'

# Function to convert RGB to Hex
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# Function to check the first four pixels and determine the background color
def get_background_color(skull_image):
    skull_pixels = skull_image.load()
    positions = [(46, 2), (46, 3), (47, 2), (47, 3)]
    colors = [skull_pixels[x, y][:3] for x, y in positions]
    
    if all(color == colors[0] for color in colors):
        return rgb_to_hex(colors[0])
    return None

# Iterate through each skull image
for skull in skulls_data:
    skull_image_path = os.path.join(images_dir, f"{skull['name']}.jpg")
    skull_image = Image.open(skull_image_path).convert("RGBA")
    
    background_color = get_background_color(skull_image)
    if background_color:
        skull['attributes']['Background'] = background_color
        print(f"Set background color for {skull['name']} to {background_color}")

# Save the updated JSON file
with open('rise-of-skulls.json', 'w') as file:
    json.dump(skulls_data, file, indent=4)
