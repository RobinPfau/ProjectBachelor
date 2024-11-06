import customtkinter as ctk

class Controls(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth, rheight, grid, matrix, **kwargs):

        #setup control menu
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
        self.button_number = 1
        self.grid = grid
        self.matrix = matrix
        self.create_numpad(colour)
        self.create_control_buttons()

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
        button_delete = ctk.CTkButton(self, text = "DELETE" ,command=  lambda: self.on_press_delete())
        button_delete.pack(padx = 10, pady= 10)

        button_load = ctk.CTkButton(self, text = "LOAD" ,command=  lambda: self.on_press_load())
        button_load.pack(padx = 10, pady= 10)
         
    #functionality of the delete button
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

    #functionality of the numpad buttons
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

    def on_press_load(self):
        #todo: load a puzzle from json through converter
        self.grid.create_grid()
        print("newGrid")
      