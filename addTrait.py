import json
import os
from PIL import Image

# Load the JSON file
with open('rise-of-skulls.json', 'r') as file:
    skulls_data = json.load(file)

# Define the directory paths
images_dir = 'images'
traits_dir = 'images/traits'

# Function to check if a trait is present in a skull image
def check_trait_in_image(trait_data, skull_image):
    skull_pixels = skull_image.load()
    
    for trait in trait_data:
        x, y = trait['position']
        r, g, b = trait['color']  # No alpha channel in the provided JSON
        if (r, g, b) != skull_pixels[x, y][:3]:
            return False
    return True

# Iterate through each skull image
for skull in skulls_data:
    skull_image_path = os.path.join(images_dir, f"{skull['name']}.jpg")
    skull_image = Image.open(skull_image_path).convert("RGBA")
    
    for trait_category in os.listdir(traits_dir):
        trait_category_path = os.path.join(traits_dir, trait_category)
        
        if os.path.isdir(trait_category_path):
            for trait_file in os.listdir(trait_category_path):
                if trait_file.endswith('.json'):
                    trait_file_path = os.path.join(trait_category_path, trait_file)
                    with open(trait_file_path, 'r') as file:
                        trait_data = json.load(file)
                    
                    trait_name = os.path.splitext(trait_file)[0]
                    if check_trait_in_image(trait_data, skull_image):
                        skull['attributes'][trait_category] = trait_name
                        print(f"Found {trait_name} in {skull['name']}")

# Save the updated JSON file
with open('rise-of-skulls.json', 'w') as file:
    json.dump(skulls_data, file, indent=4)
