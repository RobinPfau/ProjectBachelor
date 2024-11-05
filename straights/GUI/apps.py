import customtkinter as ctk

from .grid import Grid
from .controls import Controls
from .matrix import Matrix
from converter import Converter

puzzle3 = [-3,0,None,None,None,None,0,None,None,None,None,None,0,None,7,None,None,None,2,None,None,0,-1,None,9,None,None,0,None,None,None,0,None,None,None,-4,None,None,0,None,5,0,None,None,0,None,None,8,-6,None,3,0,None,None,None,None,None,None,0,None,None,None,None,None,None,-9,None,None,0,None,2,0,0,None,None,None,None,-2,None,None,-5]
puzzle4 = "000000009000000060930000000000004000003000000000720000090000200000000010100000020000000011000000000000000000011001100001100011000000000000001000001000000100000000"
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
        self.converter = Converter()
        puzzlelist = self.converter.convert(puzzle4)

        self.matrix = Matrix(puzzlelist)
        self.grid = Grid(self, 0, 0, "green", 0.65, 1, self.matrix)
        self.controls = Controls(self, 0.7, 0, "black", 0.3, 0.65, self.grid, self.matrix)
    


        #self.solver = Solver(self, 0, 0.7, "green", 0.65, 0.3)
        #print(puzzle_grid)
       
        #run
        self.mainloop()
