import customtkinter as ctk

from .grid import Grid
from .controls import Controls
from .matrix import Matrix
from .converter import Converter
from .image import Picture
from .puzzles import puzzles
from .display import Display


class App (ctk.CTk):
    def __init__(self, title, size, **kwargs):
       
       #setup app
        super().__init__(**kwargs)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")


        #sets the App Window
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(500,500)
        self.resizable(False, False)
    
        #create and use converter
       # with open("DATA/puzzles.json", "r") as file:
       #     self.puzzles = json.load(file)
        self.puzzles = puzzles
        self.converter = Converter()

        #placeholder start screen
        puzzlelist = self.converter.convert( "0"*162)
        #puzzlelist = self.converter.convert(self.puzzles["small"]["easy"]["#1"])    # add to load a puzzle directly

        #create GUI
        self.grid = Grid(parent = self, x = 0, y = 0, rwidth = 0.65, rheight = 1, puzzlelist = puzzlelist)
        self.controls = Controls(self, 0.675, 0, "black", 0.3, 1, self.grid, self.puzzles)
        self.display = Display(self, "Welcome to Str8ts",  0.675, 0.9, 0.3, 0.05)
        self.image = None #Picture(self, 700, 700)

        #run
        self.mainloop()