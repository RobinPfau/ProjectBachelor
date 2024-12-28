import customtkinter as ctk
import os
from PIL import Image

class Picture():
    def __init__(self, parent, sizex, sizey, ):
        
        image_path = os.path.join(os.path.dirname(__file__), "sigillum.png")
        self.image = ctk.CTkImage(Image.open(image_path), size= (sizex, sizey))

        self.image_label = ctk.CTkLabel(parent, image = self.image, text = "")
        self.image_label.place(x = 0, y = 0)

    def delete(self):
        self.image_label.destroy()
        