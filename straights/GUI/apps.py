import customtkinter as ctk

from .grid import Grid
from .controls import Controls
from .matrix import Matrix
from converter import Converter
from SOLVER.checker import Solver
import json

puzzle0 = "0"*162

class App (ctk.CTk):
    def __init__(self, title, size, **kwargs):
       
       #setup app
        super().__init__(**kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(500,500)
        self.resizable(False, False)
        self. matrix_size = 9
    
        #create and use converter
        with open("puzzles.json", "r") as file:
            self.puzzles = json.load(file)

        self.converter = Converter()
        puzzlelist = self.converter.convert(puzzle0)
        #puzzlelist = self.converter.convert(self.puzzles["symmetric"]["impossible"]["10.11.24"])

        #create GUI
        self.grid = Grid(parent = self, x = 0, y = 0, rwidth = 0.65, rheight = 1, puzzlelist = puzzlelist)
        self.controls = Controls(self, 0.675, 0, "black", 0.3, 0.7,self.grid, self.puzzles)
        
        #run
        self.mainloop()