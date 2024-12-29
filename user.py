import tkinter as tk
from tkinter import filedialog
import os


class User:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def change_name(self):
        root = tk.Tk()
        root.withdraw()
        new_name = tk.simpledialog.askstring("Input", "Enter new name:", parent=root)
        root.destroy()
        if new_name:
            self.name = new_name
        
    def change_image(self):
        # Get new image
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        root.destroy()
        if file_path:
            self.image = file_path
