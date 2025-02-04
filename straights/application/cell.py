import customtkinter as ctk

class Cell(ctk.CTkEntry):

    def __init__(self, *args, xcoord = 0, ycoord = 0, frame = None, locked = False,  **kwargs):
        super().__init__(*args, **kwargs) 
        self.x = xcoord           # x coordinate of the cell
        self.y = ycoord           # y coordinate of the cell
        self.locked = locked      # locked or interactive
        self.frame = frame        # frame to place the cell in
        self.color = "Blue"       # color of the cell
