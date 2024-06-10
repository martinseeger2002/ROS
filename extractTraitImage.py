import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import json

class PixelSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Selector")
        self.scale_factor = 10  # Initial scale factor for display
        self.zoom_step = 1.1  # Step for zooming in and out
        self.image_path = "./images/Skulls #5352.jpg"
        self.original_image = Image.open(self.image_path)
        self.scaled_image = self.original_image.resize(
            (self.original_image.width * self.scale_factor, self.original_image.height * self.scale_factor), 
            Image.NEAREST)
        self.photo = ImageTk.PhotoImage(self.scaled_image)

        # Create a toolbar
        toolbar = tk.Frame(root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Add Export button to the toolbar
        self.export_button = tk.Button(toolbar, text="Export", command=self.export_selected_pixels)
        self.export_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.canvas = tk.Canvas(root, width=800, height=800)  # Set canvas size as desired
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.selected_pixels = set()
        self.canvas.bind("<Button-1>", self.select_pixel)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-2>", self.pan_start)
        self.canvas.bind("<B2-Motion>", self.pan_move)

    def select_pixel(self, event):
        x, y = int(self.canvas.canvasx(event.x) / self.scale_factor), int(self.canvas.canvasy(event.y) / self.scale_factor)
        if (x, y) in self.selected_pixels:
            self.selected_pixels.remove((x, y))
            self.unhighlight_pixel(x, y)
        else:
            color = self.original_image.getpixel((x, y))
            self.selected_pixels.add((x, y, color))
            self.highlight_pixel(x, y)

    def highlight_pixel(self, x, y):
        display_x, display_y = x * self.scale_factor, y * self.scale_factor
        self.canvas.create_rectangle(display_x, display_y, display_x + self.scale_factor, display_y + self.scale_factor, outline="red", tags=f"highlight-{x}-{y}")

    def unhighlight_pixel(self, x, y):
        self.canvas.delete(f"highlight-{x}-{y}")

    def zoom(self, event):
        scale = self.zoom_step if event.delta > 0 else 1 / self.zoom_step
        self.scale_factor *= scale
        self.scaled_image = self.original_image.resize(
            (int(self.original_image.width * self.scale_factor), int(self.original_image.height * self.scale_factor)), 
            Image.NEAREST)
        self.photo = ImageTk.PhotoImage(self.scaled_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        self.refresh_highlights()

    def pan_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def pan_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def refresh_highlights(self):
        self.canvas.delete("highlight")
        for x, y, color in self.selected_pixels:
            self.highlight_pixel(x, y)

    def export_selected_pixels(self):
        selected_pixels_data = [
            {"position": (x, y), "color": color} for x, y, color in self.selected_pixels
        ]
        if not os.path.exists('./images/traits'):
            os.makedirs('./images/traits')
        save_path = filedialog.asksaveasfilename(
            initialdir='./images/traits',
            title="Save As",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
            defaultextension=".json"
        )
        if save_path:
            with open(save_path, 'w') as json_file:
                json.dump(selected_pixels_data, json_file, indent=4)
            print(f"Selected traits saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelSelectorApp(root)
    root.mainloop()
