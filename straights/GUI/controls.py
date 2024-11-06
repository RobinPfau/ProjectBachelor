import customtkinter as ctk
from converter import Converter


class Controls(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth, rheight, grid, matrix, json_keys,  **kwargs):

        #setup control menu
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
        self.button_number = 1
        self.grid = grid
        self.matrix = matrix
        self.keys = json_keys
        self.converter = Converter()

        self.create_numpad(colour)
        self.create_control_buttons()
        self.create_loading()
                
    
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
        button_solve.grid(row = 2, column = 0, fill = None, pady = 10, padx =5)

        button_help = ctk.CTkButton(frame, width = 100, text = "HELP" ,command=  lambda: self.on_press_help())
        button_help.grid(row = 2, column = 1, fill = None, pady = 10, padx =5)

        frame.pack(expand = False, fill = None, anchor = "center", padx = 10, pady = 10)
        
        #button_test = ctk.CTkButton(self, text = "TEST" ,command=  lambda: self.on_press_test())
        #button_test.pack(padx = 10, pady= 10)


    def create_loading(self):
        self.options_main = ctk.CTkOptionMenu(self, values = list(self.keys.keys()), command = self.on_press_select)
        self.options_main.set("Choose Category")
        self.options_main.pack()

        
        self.options_sub = ctk.CTkOptionMenu(self, values = ["Choose Category First"], command = self.on_press_subselect)
        self.options_sub.set("Coose Difficulty")
        self.options_sub.pack()


    #button that clears the selected cell
    def on_press_delete(self):
        focused_cell = self.grid.selected_cell
        if focused_cell is not None:
            if self.matrix.grid[focused_cell.x][focused_cell.y].value != 0:
                focused_cell.delete(0, "end")
                self.matrix.grid[focused_cell.x][focused_cell.y].value = 0
                print(self.matrix.grid[focused_cell.x][focused_cell.y].value)
                print("löscherbutton")
        else: 
            print("no active cell")

    #numpad buttons that enters the pressed number into cell
    def on_press_number(self, number):
        #print(number)
        focused_cell = self.grid.selected_cell
        if focused_cell is not None:
            focused_cell.delete(0, "end")
            focused_cell.insert(0, number)
            self.matrix.grid[focused_cell.x][focused_cell.y].value = number
            print(self.matrix.grid[focused_cell.x][focused_cell.y].value)
        else:
            print("no active cell")

    #dropdown  for puzzletype selection
    def on_press_select(self, main_cat):
        
        sub_cats = list(self.keys[main_cat].keys())
        self.options_sub.configure(values=sub_cats)
        self.options_sub.set("Select a Difficulty")
        
     #dropdown  for difficulty selection
    def on_press_subselect(self, sub_cat):
        
        selected_main = self.options_main.get()
        #self.options_main.configure(state = "disabled")
        #self.options_sub.configure(state = "disabled")

        # TODO: only selecting first puzzle in category. maybe random?
        selected_puzzle = self.converter.convert(self.keys[selected_main][sub_cat][next(iter(self.keys[selected_main][sub_cat]))])
        
        self.matrix.reload_matrix(selected_puzzle)
        self.grid.delete_grid()
        self.grid.create_grid()

        print(f"Selected path: {selected_main}/{sub_cat}")

    # TODO: start the solver and load solution into grid
    def on_press_solve(self):
        pass

    # TODO: offer a not yet defined help
    def on_press_help(self):
        pass

    # TODO: toggle to not taking in grid
    def on_press_toggle_notes(self):
        pass

        
      