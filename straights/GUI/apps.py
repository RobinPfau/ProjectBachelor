import customtkinter as ctk

from .grid import Grid
from .controls import Controls
from .matrix import Matrix
from converter import Converter
import json

puzzle0 = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
print(len(puzzle0))
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

        # creates the UI Parts in the app
        #create and use converter
        with open("puzzles.json", "r") as file:
            puzzles = json.load(file)
        self.converter = Converter()
        puzzlelist = self.converter.convert(puzzles["symmetric"]["easy"]["03.11.24"])

        #create Matrix that stores the puzzle
        self.matrix = Matrix(puzzlelist)
        #create GUI

        self.grid = Grid(self, 0, 0, "green", 0.65, 1, self.matrix)
        self.controls = Controls(self, 0.7, 0, "black", 0.3, 0.65, self.grid, self.matrix)
        


        #self.solver = Solver(self, 0, 0.7, "green", 0.65, 0.3)
        #print(puzzle_grid)
       
        #run
        self.mainloop()
