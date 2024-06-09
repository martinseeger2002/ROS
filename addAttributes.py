import json

def add_blank_attributes(filename):
    # Define the blank attributes to be added
    blank_attributes = {
        "Background": "",
        "Skull Color": "",
        "Head": "",
        "Clothes": "",
        "Mouth": "",
        "Eyes": "",
        "Nose": "",
        "Accessory": ""
    }
    
    # Read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Add the blank attributes to each entry
    for entry in data:
        entry['attributes'] = blank_attributes
    
    # Write the updated data back to the JSON file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Added blank attributes to each entry in {filename}.")

# Replace 'yourfile.json' with the actual filename
add_blank_attributes('rise-of-skulls.json')
