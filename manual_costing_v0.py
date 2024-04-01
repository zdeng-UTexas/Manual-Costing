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
        self.bg_image = Image.open(self.bg_image_path)
        self.bg_image = self.bg_image.resize((800, 800), Image.ANTIALIAS)  # Resize for the canvas
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set up canvas
        self.canvas = tk.Canvas(master, width=800, height=800)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.draw_grid()

        # Bind events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.master.bind("<p>", self.save_cost_map)

    def draw_grid(self):
        w, h = 800, 800  # Canvas size
        dx, dy = w / self.num_grid_width, h / self.num_grid_height
        for x in range(self.num_grid_width):
            self.canvas.create_line(dx * x, 0, dx * x, h)
        for y in range(self.num_grid_height):
            self.canvas.create_line(0, dy * y, w, dy * y)

    def paint(self, event):
        w, h = 800, 800  # Canvas size
        dx, dy = w / self.num_grid_width, h / self.num_grid_height
        x, y = int(event.x // dx), int(event.y // dy)
        if 0 <= x < self.num_grid_width and 0 <= y < self.num_grid_height:
            self.cost_map[y, x] = 255
            self.canvas.create_rectangle(x*dx, y*dy, (x+1)*dx, (y+1)*dy, fill="red", outline="")

    def save_cost_map(self, event):
        with open("cost_map.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for row in self.cost_map:
                writer.writerow(row)
        print("Cost map saved as cost_map.csv.")

def main():
    root = tk.Tk()
    app = CostMapCreator(root, args.num_grid_width, args.num_grid_height)
    root.mainloop()

if __name__ == "__main__":
    main()
