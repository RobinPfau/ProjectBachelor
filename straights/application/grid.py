import customtkinter as ctk
import math
from .matrix import Matrix
from .cell import Cell


class Grid(ctk.CTkFrame):
    
    def __init__(self, parent, x, y, rwidth, rheight, puzzlelist, **kwargs):
        
        #setup frame
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)

        self.selected_cell = None
        self.matrix = None
        self.cells = {}         # Store (row, col) -> Cell mappings
        self.notes = False
        self.creative_mode = False
        self.emptypuzzle = "0"*162
        self.matrix_size = int(math.sqrt(len(puzzlelist)))
        

        self.vaidate_command = parent.register(self.validate_number)

        self.create_grid(puzzlelist)

    #destroys all ctkinter elements in the grid    
    def delete_grid(self):
        self.frame.destroy()

    def create_grid(self, puzzlelist):
        self.cells.clear()
        self.matrix_size = int(math.sqrt(len(puzzlelist)))

        self.matrix = Matrix(puzzlelist)
        #puzzle frame
        self.frame = ctk.CTkFrame(self)
                
        for row in range(self.matrix_size):
            rowlist = self.matrix.grid[row]
            self.frame.grid_rowconfigure(row, weight=1)
        
            for col in range(self.matrix_size):
                self.frame.grid_columnconfigure(col, weight=1)
                
                #border_frame = ctk.CTkFrame(self.frame, fg_color = "white")
                #border_frame.grid(row=row, column=col, fill = None )          
                
                cell = Cell(self.frame, xcoord = row, ycoord = col,width = 70, height = 70, font = ("Arial", 50),justify = "center",)

                
                #bind functionality to the cells
                cell.bind("<FocusIn>", lambda event, cell = cell: self.on_click_in(event, cell))
                cell.bind("<FocusOut>", lambda event, cell = cell: self.on_click_out(event))
                cell.bind("<KeyRelease-BackSpace>", self.on_delete)
                cell.bind("<KeyRelease-Delete>", self.on_delete)
                cell.bind("<KeyRelease>", self.on_entry)

                #only arabic numerals allowed in entries
                cell.configure(validate = "key", validatecommand = (self.vaidate_command, "%P"))
                
                #cell.frame = border_frame
                content = rowlist[col]
                if content.value != 0:
                    cell.insert(0, content.value)
                cell.color = content.color
                cell.configure(fg_color = content.color, text_color = content.get_text_color(), state = content.get_state())
                if content.get_state() == "normal":
                    cell.locked = False
                else:
                    cell.locked = True
                self.cells[row,col] = cell
                #cell.grid(padx = 1,pady = 1)
                
                cell.grid(row = row, column = col, fill = None, padx = 1, pady = 1) 
                
  
        self.frame.pack(expand = False, fill= None, anchor = "nw", padx = 20, pady = 20)

    
    #select entry with mouse, indicate visually
    def on_click_in(self, event, cell):
        
        self.selected_cell = cell
        if self.creative_mode == False:
            for list in self.matrix.straights:
                for element in list:
                    if element.x == cell.x and element.y == cell.y:
                   
                        for element in list:
                            x = element.x
                            y = element.y
                        #self.cells[x,y].frame.configure(fg_color = "lightgreen")
                            self.cells[x,y].configure(fg_color = "lightgreen")

            cell.configure(fg_color = "green")

    #needed for losing focus 
    def on_click_out(self, event):
        if self.creative_mode is False:
            for x in range(self.matrix_size):
                for y in range(self.matrix_size):
                    if self.cells[x,y].cget("state") != "disabled" and self.cells[x,y].cget("fg_color") != "teal":
                        self.cells[x,y].configure(fg_color = "white")

    #functionality on typing in cell, update visual and matrix
    def on_entry(self, event):
        cell = event.widget
        
        x = self.selected_cell.x
        y = self.selected_cell.y

        if cell.get():
            current_value = cell.get()[0]
            cell.delete(0, "end")
            if event.char.isdigit() and event.char != "0" and cell.cget("state") != "readonly":
                

                if self.creative_mode == False:
                    self.selected_cell.configure(text_color = "blue")
                else:
                    if self.matrix.grid[x][y].color == "black":
                        self.selected_cell.configure(text_color = "white")
                    else:
                        self.selected_cell.configure(text_color = "black")
        
                cell.insert(0, event.char)
                self.matrix.grid[x][y].value = int(event.char)
                
                print(self.matrix.grid[x][y].value)

            elif current_value in "123456789":
                cell.insert(0, current_value)

    #button function that deletes value in highlighted cell
    def on_delete(self, event):
        x = self.selected_cell.x
        y = self.selected_cell.y
       
        if self.matrix.grid[x][y].value == 0 or self.selected_cell.cget("state") == "readonly":
            return
        
        cell = event.widget
        cell.delete(0, "end")
      
        self.matrix.grid[x][y].value = 0
        print(self.matrix.grid[x][y].value)
        print("löscher")
        #print(event.char)    

    #update the displayed value in a cell
    def update_cell(self, row, col, value):
        cell = self.cells.get((row, col))
        
        cell.delete(0, "end")
        cell.insert(0, str(value))

    #saves the solutions into the gridelements in the matrix grid
    def save_solution(self, solutions):
        for x, row in enumerate(solutions):
            for y, solution in enumerate(row):
                if solution > 0:
                    self.matrix.grid[x][y].solution = solution

    # TODO: checks if solution and value in Grid are the same
    def check_cell_solution(self):
    
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                solution = self.matrix.grid[x][y].solution
                cell = self.cells[x, y]
                if cell.get() and cell.locked == False:
                    if solution != int(cell.get()[0]):
                        cell.color = "red"
                        cell.configure(text_color = "red")

    
    #updates cell to correct value
    def reveal_cell_solution(self):
        if self.selected_cell:
            cell = self.selected_cell
            x = cell.x
            y = cell.y
            if cell.color == "red":
                cell.color = "blue"
                cell.configure(text_color = "blue")
            if self.matrix.grid[x][y].solution:
                solution = self.matrix.grid[x][y].solution
                self.matrix.update_matrix(x, y, solution)
                cell.delete(0, "end")
                cell.insert(0, str(solution))
            else:
                print("grid: no solution safed")


    #swap color of a cell in creative mode
    def swap_color(self):
        if self.selected_cell:
            cell = self.selected_cell
            x = cell.x
            y = cell.y
            color = self.matrix.grid[x][y].color
           
            if color == "white":
                cell.color = "black"
                cell.configure(fg_color = "black", text_color = "white")      
                self.matrix.grid[x][y].color = "black"
                cell.locked = True

            else:
                cell.color = "white"
                cell.configure(fg_color = "white",text_color = "black")
                self.matrix.grid[x][y].color = "white"
                cell.locked = False
        else:
            print("No Cell Selected Swap")
         
    # utility function that validates input as integer
    def validate_number(self, text):
        return text == "" or text.isdigit()