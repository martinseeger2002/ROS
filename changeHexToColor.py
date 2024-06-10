import json
import webcolors

# List of common color names and their hex values
colors = {
    "#FFFFFF": "White",
    "#C0C0C0": "Silver",
    "#808080": "Gray",
    "#000000": "Black",
    "#FF0000": "Red",
    "#800000": "Maroon",
    "#FFFF00": "Yellow",
    "#808000": "Olive",
    "#00FF00": "Lime",
    "#008000": "Green",
    "#00FFFF": "Aqua",
    "#008080": "Teal",
    "#0000FF": "Blue",
    "#000080": "Navy",
    "#FF00FF": "Fuchsia",
    "#800080": "Purple",
    "#FFA07A": "Light Salmon",
    "#FFA500": "Orange",
    "#FF4500": "Orange Red",
    "#DA70D6": "Orchid",
    "#EEE8AA": "Pale Goldenrod",
    "#98FB98": "Pale Green",
    "#AFEEEE": "Pale Turquoise",
    "#DB7093": "Pale Violet Red",
    "#FFEFD5": "Papaya Whip",
    "#FFDAB9": "Peach Puff",
    "#CD853F": "Peru",
    "#FFC0CB": "Pink",
    "#DDA0DD": "Plum",
    "#B0E0E6": "Powder Blue",
    "#BC8F8F": "Rosy Brown",
    "#4169E1": "Royal Blue",
    "#8B4513": "Saddle Brown",
    "#FA8072": "Salmon",
    "#F4A460": "Sandy Brown",
    "#2E8B57": "Sea Green",
    "#FFF5EE": "Seashell",
    "#A0522D": "Sienna",
    "#C0C0C0": "Silver",
    "#87CEEB": "Sky Blue",
    "#6A5ACD": "Slate Blue",
    "#708090": "Slate Gray",
    "#FFFAFA": "Snow",
    "#00FF7F": "Spring Green",
    "#4682B4": "Steel Blue",
    "#D2B48C": "Tan",
    "#D8BFD8": "Thistle",
    "#FF6347": "Tomato",
    "#40E0D0": "Turquoise",
    "#EE82EE": "Violet",
    "#F5DEB3": "Wheat",
    "#F5F5F5": "White Smoke",
    "#FFFF00": "Yellow",
    "#9ACD32": "Yellow Green",
}

def closest_color_name(hex_color):
    try:
        return webcolors.hex_to_name(hex_color)
    except ValueError:
        min_colors = {}
        for key in colors.keys():
            r_c, g_c, b_c = webcolors.hex_to_rgb(hex_color)
            r_n, g_n, b_n = webcolors.hex_to_rgb(key)
            rd = (r_c - r_n) ** 2
            gd = (g_c - g_n) ** 2
            bd = (b_c - b_n) ** 2
            min_colors[(rd + gd + bd)] = colors[key]
        return min_colors[min(min_colors.keys())]

def change_background_color_name(entry):
    if 'Background' in entry['attributes']:
        value = entry['attributes']['Background']
        if value.startswith('#'):
            try:
                color_name = closest_color_name(value)
                entry['attributes']['Background'] = color_name
            except ValueError:
                pass
    return entry

def main():
    with open('rise-of-skulls.json', 'r') as f:
        data = json.load(f)

    updated_data = [change_background_color_name(entry) for entry in data]

    with open('updated-rise-of-skulls.json', 'w') as f:
        json.dump(updated_data, f, indent=4)

if __name__ == "__main__":
    main()
