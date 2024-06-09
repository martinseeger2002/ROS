import json
import re

def extract_number(name):
    match = re.search(r'\d+', name)
    return int(match.group()) if match else float('inf')

def reorder_json_file(filename):
    # Read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Sort the data by the number in the 'name' field
    sorted_data = sorted(data, key=lambda x: extract_number(x['name']))
    
    # Write the sorted data back to the JSON file
    with open(filename, 'w') as file:
        json.dump(sorted_data, file, indent=4)
    
    print(f"Reordered entries in {filename} by number in the 'name' field.")

# Replace 'yourfile.json' with the actual filename
reorder_json_file('rise-of-skulls.json')
