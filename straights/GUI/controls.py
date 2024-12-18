import customtkinter as ctk
from DATA.converter import Converter
from SOLVER.smt_v1 import SmtSolver
from SOLVER.creator_v2 import SmtCreator
from SOLVER.smt_v2 import SmtSolver_v2
import random as random

class Controls(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth, rheight, grid, json_keys, **kwargs):

        #setup control menu
        super().__init__(parent, **kwargs)
        self. parent = parent
        self.matrix_size = 9
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

        button_check = ctk.CTkButton(frame, width = 100, text = "CHECK" ,command=  lambda: self.on_press_check())
        button_check.grid(row = 1, column = 1, fill = None, pady = 10, padx =5)

        button_reveal = ctk.CTkButton(frame, width = 100, text = "REVEAL" ,command=  lambda: self.on_press_reveal())
        button_reveal.grid(row = 2, column = 0, fill = None, pady = 10, padx =5)
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

    # creates creative mode interface
    def create_creative_buttons(self):
        frame = ctk.CTkFrame(self)

        for row in range(3):
             for col in range(2):
                frame.grid_rowconfigure(row, weight=1)
                frame.grid_columnconfigure(col, weight=1)

        self.button_creative = ctk.CTkButton(frame, width = 100, text = "CREATIVE MODE" ,command=  lambda: self.on_press_creative_mode())
        self.button_creative.grid(row = 0, column = 0, fill = None, pady = 10, padx =5)
        
        self.button_swap_color = ctk.CTkButton(frame, fg_color = "darkgreen", width = 100, text = "SWAP COLOR" ,command = lambda: self.on_press_swap_color())
        
        self.button_save_creative = ctk.CTkButton(frame, fg_color = "darkgreen", width = 100, text = "EXPORT Puzzle" ,command = lambda: self.on_press_save())

        self.button_solve_creative = ctk.CTkButton(frame, fg_color = "darkgreen", width = 100, text = "SOLVE Puzzle" ,command = lambda: self.on_press_solve_creative())

        self.button_load_creative = ctk.CTkButton(frame, fg_color = "darkgreen", width = 100, text = "LOAD Puzzle" ,command = lambda: self.on_press_load())

        
       
        frame.pack(expand = False, fill = None, anchor = "s", padx = 10, pady = 10)

    #functionality of numberpad    
    def on_press_number(self, number):
        focused_cell = self.grid.selected_cell
             
        if focused_cell is not None and focused_cell.cget("state") != "readonly":
            focused_cell.delete(0, "end")
            focused_cell.insert(0, number)
            matrix_cell = self.grid.matrix.grid[focused_cell.x][focused_cell.y]
            matrix_cell.value = number

            if self.grid.creative_mode == False:
                focused_cell.configure(text_color = "blue")
            else:
                if matrix_cell.color == "black":
                    focused_cell.configure(text_color = "white")
                else:
                    focused_cell.configure(text_color = "black")
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
        
        
        print(f"Selected path: {selected_main}/{sub_cat}")

        self.load_puzzle(selected_puzzle)

        self.solutions = self.solve()
        
        if self.solutions:
            self.grid.save_solution(self.solutions)
    
    #loads a new grid with provided puzzle and attempts to find a solution
    def load_puzzle(self, selected_puzzle):
        if self.parent.image:
            self.parent.image.delete()

        self.grid.delete_grid()
        self.grid.create_grid(selected_puzzle)

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

        smt_v2 = SmtSolver_v2()
        solutions = smt_v2.solve(self.puzzlestring)
       
        #smt_v1 = SmtSolver(self.puzzlestring, self.grid.matrix, self.matrix_size)
        #solutions = smt_v1.find_grid()
        if solutions:
            has_alternate = smt_v2.alternate_solution()
        return solutions

    #loads the solution into the GUI
    def on_press_solve(self):
        
        if self.solutions:
            for row in range(self.matrix_size):
                for col in range(self.matrix_size):
                    cell = self.grid.cells.get((row,col))
                    
                    value = self.solutions[row][col]
                
                    if cell.locked == False:
                        self.grid.matrix.grid[row][col].value = value
                        cell.delete(0, "end")
                        cell.insert(0, str(value))
                        cell.configure(text_color = "blue")
        else: 
            print("error solution none")     

    #checks if the active sell holds the correct value
    def on_press_check(self):
        self.grid.check_cell_solution()

    #reveals the correct value in the selected cell
    def on_press_reveal(self):
       self.grid.reveal_cell_solution()

    # TODO: offer a not yet defined help
    def on_press_help(self):

        #solver = SmtSolver_v2()
        #value = solver.solve_single(self.puzzlestring, 4, 4)

        creator = SmtCreator(self.matrix_size)
       
        puzzlestring = creator.create_puzzle()
        print(puzzlestring)
        puzzlelist = self.converter.convert(puzzlestring)
        self.grid.delete_grid()
        self.grid.create_grid(puzzlelist)
        
    # TODO: toggle to not taking in grid
    def on_press_toggle_notes(self):
        pass        
      
    #starts the creative mode, disables map selection  
    def on_press_creative_mode(self):
        if self.grid.creative_mode == True:
            self.button_swap_color.grid_forget()
            self.button_save_creative.grid_forget()
            self.button_solve_creative.grid_forget()
            self.button_load_creative.grid_forget()
            
            self.button_creative.configure(fg_color = ['#3a7ebf', '#1f538d'])
            self.options_main.configure(state = "normal")

            self.puzzlestring = self.save_string()

            self.grid.creative_mode = False
            if self.puzzlestring:
                self.solutions = self.solve()
            if self.solutions:
                self.grid.save_solution(self.solutions)

            for x in range(self.matrix_size):
                rowlist = self.grid.matrix.grid[x]
                for y in range(self.matrix_size):
                    content = rowlist[y]
                    self.grid.cells[x,y].configure(fg_color = content.color, text_color = content.get_text_color(), state = content.get_state())



        else:
            self.load_puzzle(self.converter.convert("0"*162))

            self.button_swap_color.grid(row = 1, column = 0, fill = None, pady = 10, padx =5)
            self.button_save_creative.grid(row = 1, column = 1, fill = None, pady = 10, padx =5)
            self.button_solve_creative.grid(row = 0, column = 1, fill = None, pady = 10, padx =5)
            self.button_load_creative.grid(row = 2, column = 0, fill = None, pady = 10, padx =5)

            self.button_creative.configure(fg_color = "darkgreen")

            self.grid.creative_mode = True
            self.options_main.configure(state = "disabled")
            self.options_sub.configure(state = "disabled")
    
    #TODO: Create confirmation for swapping modes
    #def confirm_switch(self):
     #   response = messagebox.askyesno("Confirm Switch", "Are you sure= Unsaved Progress will be lost.")
     #  if response:
      #      self.switch.mode()
      #  else: 
       #     print("switch cancelled")


    #swaps black to white and back for creative mode
    def on_press_swap_color(self):
        if self.grid.selected_cell:
            self.grid.swap_color()

    #TODO: for now prints the created puzzle as a string
    #      should save the string to be loaded later
    def on_press_save(self):
        self.save_string()

    #returns the string of the puzzle created
    def save_string(self):
        puzzlestring = ""
        intstring = ""
        colorstring = ""
        for row in self.grid.matrix.grid:
            for col in row:
                value =  str(col.value)
                if col.color == "black":
                    color = "1"
                else:
                    color =  "0"
                intstring += value
                colorstring += color

        puzzlestring = intstring + colorstring
       
        print(puzzlestring)
        return (puzzlestring)
    

    def on_press_solve_creative(self):
        self.grid.matrix.find_straights()
        self.puzzlestring = self.save_string()
        self.solutions = self.solve()

        if self.solutions:
            self.grid.save_solution(self.solutions)

        self.on_press_solve()

    # this is the load interface (maybee export to class)
    def on_press_load(self):
        popup = ctk.CTkToplevel(self.parent)  
        popup.geometry("400x200")
        popup.title("Import Window")
        popup.attributes("-topmost", True)

        def load_and_pass_entry():
            entry_text = text_field.get()
            colorstring = entry_text[81:]
            if len(entry_text) == 162 and entry_text.isdigit() and set(colorstring) <= {"0", "1"}:
                popup.destroy()  # Close the popup after getting the text
                self.pass_and_load(entry_text)  # Pass the entry text to the callback function
            else:
                print("wrong length or not number")
            
        # Add widgets to the popup
        label = ctk.CTkLabel(popup, text="Enter a PuzzleString here:")
        label.pack(pady = 20, padx = 10)

        input_frame = ctk.CTkFrame(popup)
        input_frame.pack(pady=10, padx=10, fill="x")

        text_field = ctk.CTkEntry(input_frame)
        text_field.pack(side="left", fill="x", expand=True, padx=(0, 10))

        print_button = ctk.CTkButton(input_frame, text="Load", width = 40, command=load_and_pass_entry)
        print_button.pack(side="right")

        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady =10, padx = 10)


    #loads the entered string as a puzzle
    def pass_and_load(self, input_string):
        self.grid.delete_grid()

        input_list = self.converter.convert(input_string)
        self.grid.create_grid(input_list)
        self.puzzlestring = input_string

        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                self.grid.cells[x,y].configure(state = "normal")
        self.grid.cells
        print(f"Popup Entry content: {input_string}")