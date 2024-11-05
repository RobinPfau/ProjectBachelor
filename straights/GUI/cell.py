import customtkinter as ctk

class Cell(ctk.CTkEntry):

    def __init__(self, *args, xcoord = 0, ycoord = 0, **kwargs):
        super().__init__(*args, **kwargs) 
        self.x = xcoord
        self.y = ycoord
