import tkinter as tk
from tkinter import filedialog


class User:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def change_name(self):
        root = tk.Tk()
        root.withdraw()
        new_name = tk.simpledialog.askstring("Input", "Enter new name:", parent=root)
        if new_name:
            self.name = new_name

    def change_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.image = file_path
