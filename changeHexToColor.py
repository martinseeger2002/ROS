import json
import os
from colorsys import rgb_to_hsv

# Load the JSON file
with open('rise-of-skulls.json', 'r') as file:
    skulls_data = json.load(file)

# Define a list of 20 colors with their RGB values
color_names = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Orange": (255, 165, 0),
    "Pink": (255, 192, 203),
    "Purple": (128, 0, 128),
    "Brown": (165, 42, 42),
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Gray": (128, 128, 128),
    "Light Blue": (173, 216, 230),
    "Light Green": (144, 238, 144),
    "Light Gray": (211, 211, 211),
    "Dark Blue": (0, 0, 139),
    "Dark Green": (0, 100, 0),
    "Dark Gray": (169, 169, 169),
    "Dark Red": (139, 0, 0)
}

# Function to convert hex to RGB
def hex_to_rgb(hex_color):
    if not hex_color.startswith("#") or len(hex_color) != 7:
        raise ValueError("Invalid hex color")
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Function to calculate the hue of an RGB color
def rgb_to_hue(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = rgb_to_hsv(r, g, b)
    return h

# Function to find the closest color name based on hue
def closest_color_name(hex_color):
    try:
        target_rgb = hex_to_rgb(hex_color)
    except ValueError:
        return None

    target_hue = rgb_to_hue(target_rgb)
    
    min_diff = float('inf')
    closest_color = None
    for color_name, color_rgb in color_names.items():
        color_hue = rgb_to_hue(color_rgb)
        diff = abs(target_hue - color_hue)
        if diff < min_diff:
            min_diff = diff
            closest_color = color_name
    return closest_color

# Iterate through each skull entry and update the Background color
for skull in skulls_data:
    hex_color = skull['attributes'].get('Background', '')
    if hex_color:
        closest_color = closest_color_name(hex_color)
        if closest_color:
            skull['attributes']['Background'] = closest_color
            print(f"Updated {skull['name']} background to {closest_color}")

# Save the updated JSON file
with open('rise-of-skulls-updated.json', 'w') as file:
    json.dump(skulls_data, file, indent=4)
