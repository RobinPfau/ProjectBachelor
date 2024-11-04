import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
 
puzzle1 = "-3x0000x00000x07000200x-10900x000x000-400x04x00x008-603x000000x000000900x01xx0000-200-5"
puzzle_grid = []
class App (ctk.CTk):
    def __init__(self, title, size, **kwargs):
       
       #setup app
        super().__init__(**kwargs)

        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(500,500)
        self.resizable(False, False)

        #widgets
        self.Puzzle = Puzzle(self, 0, 0, "green", 0.65, 0.65)
        self.Controls = Controls(self, 0.7, 0, "black", 0.3, 0.65)
        self.Controls = Solver(self, 0, 0.7, "green", 0.65, 0.3)
        print(puzzle_grid)
       

        #run
        self.mainloop()

class Puzzle(ctk.CTkFrame):
    
    def __init__(self, parent, x, y, colour, rwidth,  rheight, **kwargs):
        
        #setup frame
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
        self.selected_entry = None
        self.create_grid()
        
    def create_grid(self):
        #puzzle frame
        frame = ctk.CTkFrame(self, )
        contentcounter = 0

        for row in range(9):
            current_row = []
            for col in range(9):

                frame.grid_rowconfigure(row, weight=1)
                frame.grid_columnconfigure(col, weight=1)
                cell = ctk.CTkEntry(frame, width = 40, height = 40, font=("Arial", 24), justify = "center")
                cell.bind("<FocusIn>", self.on_click)
                content = puzzle1[contentcounter]
                current_row.append(content) 
                if content == "x":
                    cell.configure(fg_color = "black", text_color = "white", state = "disabled")
                elif content == "0":
                    cell.configure(fg_color = "white", text_color = "black")
                elif content == "-":
                    contentcounter = contentcounter + 1
                    content = puzzle1[contentcounter]
                    cell.insert(0, content)    
                    cell.configure(fg_color = "black", text_color = "white", state = "disabled")
                else:     
                    cell.insert(0, content)
                    cell.configure(fg_color = "white" , text_color = "black", state = "disabled")
                
                cell.grid(row = row, column = col, fill = None,)           
                contentcounter = contentcounter + 1

            puzzle_grid.append(current_row)    

        frame.pack(expand = False, fill= None, anchor = "nw", padx = 10, pady = 10)
    
    #select entry with mouse
    def on_click(self, event):
        self.selected_entry = event.widget
        print("selected a cell")
        


class Controls(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth, rheight, **kwargs):

        #setup control menu
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
    
        #making the numpad
        frame = ctk.CTkFrame(self, )
        buttonnumber = 1
        for row in range(3):
             for col in range(3):
                
                frame.grid_rowconfigure(row, weight=1)
                frame.grid_columnconfigure(col, weight=1)

                button = ctk.CTkButton(frame, fg_color = colour)
                button.configure(text = buttonnumber)
                buttonnumber = buttonnumber + 1
                button.grid(row = row, column = col, fill = None)

       
        frame.pack(expand = False, fill= None, anchor = "center", padx = 10, pady = 10)

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