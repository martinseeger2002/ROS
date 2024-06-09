import os
import cv2
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

# Define the path to your image directory
image_dir = './images'  # Update this to your actual image directory

# Ensure the directory exists
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Initialize global variables
selected_region = None
current_image_path = None

# Function to handle the rectangle selector
def onselect(eclick, erelease):
    global selected_region
    x1, y1 = int(eclick.xdata), int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)
    selected_region = (x1, y1, x2, y2)
    plt.close()

# Function to load and display an image with an interactive rectangle selector
def load_and_display_image(image_path):
    global current_image_path
    current_image_path = image_path
    image = Image.open(image_path)
    fig, ax = plt.subplots(1)
    ax.imshow(image)
    rect_selector = RectangleSelector(
        ax, onselect, useblit=True,
        button=[1],  # Left mouse button
        minspanx=5, minspany=5, spancoords='pixels',
        interactive=True
    )
    print(f"Displaying image: {image_path}")
    plt.show()

# Function to extract the selected region and name the trait
def label_trait():
    global selected_region, current_image_path
    if selected_region and current_image_path:
        x1, y1, x2, y2 = selected_region
        image = cv2.imread(current_image_path)
        trait_region = image[y1:y2, x1:x2]
        plt.imshow(cv2.cvtColor(trait_region, cv2.COLOR_BGR2RGB))
        plt.title("Selected Trait Region")
        plt.show()
        trait_name = input("Enter the trait name: ")
        return trait_name, trait_region
    return None, None

# Function to match the trait region in the rest of the images
def match_trait(trait_region, image_path):
    image = cv2.imread(image_path)
    result = cv2.matchTemplate(image, trait_region, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)
    if len(loc[0]) > 0:
        return True
    return False

# Function to process and label all images
def process_and_label_images(image_dir):
    labeled_data = {}
    traits_regions = {}
    
    for i in range(1, 5778):
        image_file = f"Skulls #{i}.jpg"
        image_path = os.path.join(image_dir, image_file)
        if os.path.exists(image_path):
            load_and_display_image(image_path)
            trait_name, trait_region = label_trait()
            if trait_name and trait_region is not None:
                traits_regions[trait_name] = trait_region
                labeled_data[image_file] = {trait_name: True}
            else:
                labeled_data[image_file] = {}
            
            # Compare the selected trait region with other images
            for j in range(1, 5778):
                other_image_file = f"Skulls #{j}.jpg"
                other_image_path = os.path.join(image_dir, other_image_file)
                if os.path.exists(other_image_path) and other_image_file != image_file:
                    if match_trait(trait_region, other_image_path):
                        if other_image_file not in labeled_data:
                            labeled_data[other_image_file] = {}
                        labeled_data[other_image_file][trait_name] = True
    
    return labeled_data

# Process and label images
labeled_traits_data = process_and_label_images(image_dir)

# Save the labeled traits data to a JSON file
output_file = os.path.join(image_dir, 'labeled_traits_data.json')
with open(output_file, 'w') as outfile:
    json.dump(labeled_traits_data, outfile, indent=4)

print(f"Traits labeling completed and saved to {output_file}")
