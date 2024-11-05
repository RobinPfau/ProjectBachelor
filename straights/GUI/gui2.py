import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
 
puzzle1 = "-3x0000x00000x07000200x-10900x000x000-400x04x00x008-603x000000x000000900x01xx0000-200-5"

puzzle2 = "cx0000x00000x07000200xa0900x000x000d00x04x00x008f03x000000x000000900x01xx0000b00e"

puzzle3 = [-3,0,None,None,None,None,0,None,None,None,None,None,0,None,7,None,None,None,2,None,None,0,-1,None,9,None,None,0,None,None,None,0,None,None,None,-4,None,None,0,None,5,0,None,None,0,None,None,8,-6,None,3,0,None,None,None,None,None,None,0,None,None,None,None,None,None,-9,None,None,0,None,2,0,0,None,None,None,None,-2,None,None,-5]

puzzle_grid = []

class App (ctk.CTk):
    def __init__(self, title, size, **kwargs):
       
       #setup app
        super().__init__(**kwargs)

        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(500,500)
        self.resizable(False, False)

        # creates the UI Parts in the app
        self.matrix = Matrix(puzzle3)
        self.grid = Grid(self, 0, 0, "green", 0.65, 0.65, self.matrix)
        self.controls = Controls(self, 0.7, 0, "black", 0.3, 0.65, self.grid, self.matrix)
    


        #self.solver = Solver(self, 0, 0.7, "green", 0.65, 0.3)
        #print(puzzle_grid)
       

        #run
        self.mainloop()
#creates a 2D Matrix of the Puzzle
class Matrix():
    def __init__(self, puzzle):
        self.grid = []
        self.grid_content = None
        counter = 0
        for row in range(9):
            current_row = []
            for col in range(9):
                self.grid_content = puzzle[counter]
                current_row.append(self.grid_content)
                counter += 1
                
            self.grid.append(current_row)
        print(self.grid)

    def update_matrix(x,y,n):
        return
   
#create the str8ts grid and fills the matrix on entries
class Grid(ctk.CTkFrame):
    
    def __init__(self, parent, x, y, colour, rwidth,  rheight, matrix: Matrix, **kwargs):
        
        #setup frame
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
        self.selected_entry = [None,None]
        self.selected_cell = None
        self.matrix = matrix
        self.create_grid()


    def create_grid(self):
        #puzzle frame
        frame = ctk.CTkFrame(self)
                
        for row in range(9):
            rowlist = self.matrix.grid[row]
            frame.grid_rowconfigure(row, weight=1)
        
            for col in range(9):
                frame.grid_columnconfigure(col, weight=1)
                
                border_frame = ctk.CTkFrame(frame, fg_color = "white")
                border_frame.grid(row=row, column=col, fill = None )          
                
                cell = Cell(border_frame, xcoord = row, ycoord = col, width = 40, height = 40, font = ("Arial", 24),justify = "center",)

                cell.bind("<FocusIn>", lambda event, frame=border_frame, row = row, col = col, cell = cell: self.on_click_in(event, frame, row, col, cell))
                cell.bind("<FocusOut>", lambda event, frame=border_frame: self.on_click_out(event, frame))
                cell.bind("<KeyRelease>", self.on_entry)
                
                content = rowlist[col]

                if content == None:
                    cell.configure(fg_color = "white", text_color = "blue")
                elif content == 0:
                    cell.configure(fg_color = "black", text_color = "white", state = "disabled")
                elif content > 0:
                    cell.insert(0,content)
                    cell.configure(fg_color = "white", text_color = "black", state = "disabled")
                elif content < 0:
                    cell.insert(0,-content)
                    cell.configure(fg_color = "black", text_color = "white", state = "disabled")
                else:
                    print("error in puzzlelist")             
                cell.pack(padx = 1,pady = 1)
                #cell.grid(row = row, column = col, fill = None,) 
                
  
        frame.pack(expand = False, fill= None, anchor = "nw", padx = 10, pady = 10)
    
    
#select entry with mouse
    def on_click_in(self, event, frame,x ,y, cell):
        frame.configure(fg_color = "lightgreen")
        self.selected_entry = [x,y]
        self.selected_cell = cell
        #print(self.selected_entry)
        #print(cell.x) 
        #print("selected a cell")

    def on_click_out(self, event, frame):
        frame.configure(fg_color = "white")

    #on typing in cell, update visual and matrix
    def on_entry(self, event):
        cell = event.widget

        x = self.selected_entry[0]
        y = self.selected_entry[1]
    
   
        current_value = cell.get()[0]
        cell.delete(0, "end")
        if event.char in "123456789":
            cell.insert(0, event.char)
            self.matrix.grid[x][y] = event.char
            #print(self.matrix.grid[x][y])
            print(self.matrix.grid)
        else:
            if current_value in "123456789":
                cell. insert(0, current_value)
        
        # enter the value into backend
        #print(event.char)    


class Cell(ctk.CTkEntry):

    def __init__(self, *args, xcoord = 0, ycoord = 0, **kwargs):
        super().__init__(*args, **kwargs) 
        self.x = xcoord
        self.y = ycoord

    
class Controls(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth, rheight, grid, matrix, **kwargs):

        #setup control menu
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
        self.button_number = 1
        self.grid = grid
        self.matrix = matrix
        self.create_buttons(colour)

    def create_buttons(self, colour):
        
        #making the numpad
        frame = ctk.CTkFrame(self, )
    
        for row in range(3):
             for col in range(3):
                
                frame.grid_rowconfigure(row, weight=1)
                frame.grid_columnconfigure(col, weight=1)

                button = ctk.CTkButton(frame, fg_color = colour, text = self.button_number, command=lambda number= self.button_number: self.on_press(number))
                self.button_number =self.button_number +1
               
                button.grid(row = row, column = col, fill = None)

       
        frame.pack(expand = False, fill= None, anchor = "center", padx = 10, pady = 10)


    def on_press(self, number):
        print(number)
        focused_cell = self.grid.selected_cell

        focused_cell.delete(0, "end")
        focused_cell.insert(0, number)
        self.matrix.grid[focused_cell.x][focused_cell.y] = number
        print(self.matrix.grid)
        #self.matrix.grid[x][y] = number
        #print(self.matrix.grid[x][y])
            #print(self.matrix.grid)


class Solver(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth, rheight, **kwargs):

        #setup solver menu
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
    
        #making the solver controls
        frame = ctk.CTkFrame(self, )
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        button_solve = ctk.CTkButton(frame, fg_color = colour, text="solve")
        button_load = ctk.CTkButton(frame, fg_color = "dark green", text="load")
        button_solve.grid(row = 0, column = 0, fill = None)
        button_load.grid(row = 1, column = 0, fill = None)


        frame.pack(expand = False, fill= None, anchor = "center", padx = 10, pady = 10)

App("Str8ts Solver", (500,500))