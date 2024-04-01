import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import argparse
import csv

# Parse command line arguments
parser = argparse.ArgumentParser(description="Create a cost map on top of a background image.")
parser.add_argument("-num_grid_width", type=int, help="Number of grids in the width direction.")
parser.add_argument("-num_grid_height", type=int, help="Number of grids in the height direction.")
args = parser.parse_args()

class CostMapCreator:
    def __init__(self, master, num_grid_width, num_grid_height):
        self.master = master
        self.num_grid_width = num_grid_width
        self.num_grid_height = num_grid_height
        self.cost_map = np.zeros((num_grid_height, num_grid_width))
        
        # Load background image
        self.bg_image_path = filedialog.askopenfilename(filetypes=[("PNG images", "*.png")])
        self.original_bg_image = Image.open(self.bg_image_path)
        self.bg_image = self.original_bg_image
        
        # Set up canvas
        self.canvas = tk.Canvas(master)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Make the canvas expandable
        
        self.update_canvas_and_grid()

        # Bind events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.master.bind("<p>", self.save_cost_map)
        self.master.bind("<Configure>", self.on_resize)  # Bind resize event

    def draw_grid(self):
        self.canvas.delete("grid_line")  # Remove old grid lines
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        dx, dy = w / self.num_grid_width, h / self.num_grid_height
        for x in range(self.num_grid_width):
            self.canvas.create_line(dx * x, 0, dx * x, h, tags="grid_line")
        for y in range(self.num_grid_height):
            self.canvas.create_line(0, dy * y, w, dy * y, tags="grid_line")

    def update_canvas_and_grid(self):
        # Remove previous image and grid before redrawing
        self.canvas.delete("bg_image")
        self.canvas.delete("grid_line")
        
        # Get the dimensions of the canvas
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w == 1 or h == 1:  # Avoid resizing to a minimal value on initialization
            return
        
        # Determine the new size of the image, preserving the square aspect ratio
        image_size = min(w, h)  # Choose the smaller dimension to fit the image
        
        # Resize the image proportionally
        self.bg_image = self.original_bg_image.resize((image_size, image_size), Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Calculate position to center the image
        x_pos = (w - image_size) // 2
        y_pos = (h - image_size) // 2
        
        # Place the centered image
        self.canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.bg_photo, tags="bg_image")
        
        self.draw_grid()

    def on_resize(self, event=None):
        # Called when the window is resized
        self.update_canvas_and_grid()

    def paint(self, event):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        dx, dy = w / self.num_grid_width, h / self.num_grid_height
        x, y = int(event.x // dx), int(event.y // dy)
        if 0 <= x < self.num_grid_width and 0 <= y < self.num_grid_height:
            self.cost_map[y, x] = 255
            self.canvas.create_rectangle(x*dx, y*dy, (x+1)*dx, (y+1)*dy, fill="red", outline="", tags="grid_paint")

    def save_cost_map(self, event):
        with open("cost_map.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for row in self.cost_map:
                writer.writerow(row)
        print("Cost map saved as cost_map.csv.")

def main():
    root = tk.Tk()
    root.attributes('-zoomed', True)
    # root.attributes('-fullscreen', True) 
    app = CostMapCreator(root, args.num_grid_width, args.num_grid_height)
    root.mainloop()

if __name__ == "__main__":
    main()
