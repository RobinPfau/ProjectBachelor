import customtkinter as ctk
from converter import Converter
from SOLVER.smt_v1 import SmtSolver
import random as random

class Controls(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth, rheight, grid, json_keys, **kwargs):

        #setup control menu
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
        self.button_number = 1
        self.grid = grid
        self.keys = json_keys
        self.solutions = None
        
               
        self.converter = Converter()

        self.create_numpad(colour)
        self.create_control_buttons()
        self.create_loading()
        self.create_creative_buttons()
                
    #creates the numpad
    def create_numpad(self, colour):
        
        #making the numpad
        frame = ctk.CTkFrame(self, )
    
        for row in range(3):
             for col in range(3):
                
                frame.grid_rowconfigure(row, weight=1)
                frame.grid_columnconfigure(col, weight=1)

                button = ctk.CTkButton(frame, width = 80, height = 70, fg_color = colour, text = self.button_number, font = ("Arial", 40), command=lambda number= self.button_number: self.on_press_number(number))
                self.button_number = self.button_number +1
               
                button.grid(row = row, column = col, fill = None)

       
        frame.pack(expand = False, fill = None, anchor = "center", padx = 10, pady = 10)

    #creates the delete button and maybe more
    def create_control_buttons(self):

        frame = ctk.CTkFrame(self, )

        for row in range(3):
             for col in range(2):
                frame.grid_rowconfigure(row, weight=1)
                frame.grid_columnconfigure(col, weight=1)


        button_delete = ctk.CTkButton(frame, width = 100, text = "DELETE" ,command=  lambda: self.on_press_delete())
        button_delete.grid(row = 0, column = 0, fill = None, pady = 10, padx =5)

        button_notes = ctk.CTkButton(frame, width = 100, text = "NOTES" ,command=  lambda: self.on_press_toggle_notes())
        button_notes.grid(row = 0, column = 1, fill = None, pady = 10, padx =5)

        button_solve = ctk.CTkButton(frame, width = 100, text = "SOLVE" ,command=  lambda: self.on_press_solve())
        button_solve.grid(row = 1, column = 0, fill = None, pady = 10, padx =5)

        button_solve = ctk.CTkButton(frame, width = 100, text = "CHECK" ,command=  lambda: self.on_press_check())
        button_solve.grid(row = 1, column = 1, fill = None, pady = 10, padx =5)

        button_solve = ctk.CTkButton(frame, width = 100, text = "REVEAL" ,command=  lambda: self.on_press_reveal())
        button_solve.grid(row = 2, column = 0, fill = None, pady = 10, padx =5)
        #creates the help button
        button_help = ctk.CTkButton(frame, width = 100, text = "HELP" ,command=  lambda: self.on_press_help())
        button_help.grid(row = 2, column = 1, fill = None, pady = 10, padx =5)

        frame.pack(expand = False, fill = None, anchor = "center", padx = 10, pady = 10)
        
        #button_test = ctk.CTkButton(self, text = "TEST" ,command=  lambda: self.on_press_test())
        #button_test.pack(padx = 10, pady= 10)

    #creates the menues used for loading puzzles
    def create_loading(self):
        self.options_main = ctk.CTkOptionMenu(self, values = list(self.keys.keys()), command = self.on_press_select)
        self.options_main.set("Choose Category")
        self.options_main.pack()

        
        self.options_sub = ctk.CTkOptionMenu(self, values = ["Choose Category First"], command = self.on_press_subselect)
        self.options_sub.set("Coose Difficulty")
        self.options_sub.pack()
        self.options_sub.configure(state = "disabled")

    def create_creative_buttons(self):
        frame = ctk.CTkFrame(self)

        for row in range(2):
             for col in range(2):
                frame.grid_rowconfigure(row, weight=1)
                frame.grid_columnconfigure(col, weight=1)

        self.button_creative = ctk.CTkButton(frame, width = 100, text = "CREATIVE MODE" ,command=  lambda: self.on_press_creative_mode())
        self.button_creative.grid(row = 0, column = 0, fill = None, pady = 10, padx =5)
        
        self.button_swap_color = ctk.CTkButton(frame, width = 100, text = "SWAP COLOR" ,command=  lambda: self.on_press_swap_color())
        #button_swap_color.grid(row = 1, column = 0, fill = None, pady = 10, padx =5)
        
       
        frame.pack(expand = False, fill = None, anchor = "s", padx = 10, pady = 10)
        
    def on_press_number(self, number):
        #print(number)
        focused_cell = self.grid.selected_cell
        if focused_cell is not None and focused_cell.cget("state") != "readonly":
            focused_cell.delete(0, "end")
            focused_cell.insert(0, number)
            self.grid.matrix.grid[focused_cell.x][focused_cell.y].value = number
            print(self.grid.matrix.grid[focused_cell.x][focused_cell.y].value)
        else:
            print("no active cell")

    #dropdown  for puzzletype selection
    def on_press_select(self, main_cat):
        
        sub_cats = list(self.keys[main_cat].keys())
        self.options_sub.configure(values=sub_cats)
        self.options_sub.set("Select a Difficulty")
        self.options_sub.configure(state = "normal")

     #dropdown  for difficulty selection
    def on_press_subselect(self, sub_cat):
        selected_main = self.options_main.get()

        self.puzzlestring = random.choice(list(self.keys[selected_main][sub_cat].values()))
        selected_puzzle = self.converter.convert(self.puzzlestring)
        
        self.grid.delete_grid()
        self.grid.create_grid(selected_puzzle)

        print(f"Selected path: {selected_main}/{sub_cat}")

        self.solutions = self.solve()
        if self.solutions:
            self.grid.save_solution(self.solutions)

    #button that clears the selected cell
    def on_press_delete(self):
        focused_cell = self.grid.selected_cell
        if focused_cell is not None and focused_cell.cget("state") != "readonly":
            if self.grid.matrix.grid[focused_cell.x][focused_cell.y].value != 0 :
                focused_cell.delete(0, "end")
                self.grid.matrix.grid[focused_cell.x][focused_cell.y].value = 0
                print(self.grid.matrix.grid[focused_cell.x][focused_cell.y].value)
                print("löscherbutton")
        else: 
            print("no active cell")
    
    #solves the selected puzzle
    def solve(self):
        smt_v1 = SmtSolver(self.puzzlestring, self.grid.matrix, 9)
        solutions = smt_v1.find_grid()
        
        return solutions

    #loads the solution into the GUI
    def on_press_solve(self):
        
        if self.solutions:
            for row in range(9):
                for col in range(9):
                    cell = self.grid.cells.get((row,col))
                    value = self.solutions[row][col]
                
                    if cell.locked == False:
                        self.grid.matrix.grid[row][col].value = value
                        cell.delete(0, "end")
                        cell.insert(0, str(value))
        else: 
            print("error solution none")     

    # TODO: checks if the active sell holds the correct value
    def on_press_check(self):
        self.grid.check_cell_solution()

    # TODO. reveals the correct value in the selected cell
    def on_press_reveal(self):
       self.grid.reveal_cell_solution()

    # TODO: offer a not yet defined help
    def on_press_help(self):
        pass
        
    # TODO: toggle to not taking in grid
    def on_press_toggle_notes(self):
        pass        
      
    def on_press_creative_mode(self):
        if self.grid.creative_mode == True:
            self.button_swap_color.grid_forget()
            
            self.button_creative.configure(fg_color = ['#3a7ebf', '#1f538d'])
            self.grid.creative_mode = False
            print("leaving")

        else:
            self.button_swap_color.grid(row = 1, column = 0, fill = None, pady = 10, padx =5)
            self.button_creative.configure(fg_color = "darkgreen")
            self.grid.creative_mode = True

    def on_press_swap_color(self):
        self.grid.swap_color()