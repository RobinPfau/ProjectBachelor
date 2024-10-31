import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
 
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
        self.Controls = Controls(self, 0.7, 0, "red", 0.3, 1)

        #run
        self.mainloop()

class Puzzle(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth,  rheight, **kwargs):
        
        #setup frame
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
    
        
        #puzzle frame
        frame = ctk.CTkFrame(self, )
        
        for row in range(9):
             for col in range(9):

                frame.grid_rowconfigure(row, weight=1)
                frame.grid_columnconfigure(col, weight=1)

                cell = ctk.CTkEntry(frame, width = 40, height = 40, font=("Arial", 24), justify = "center")
                cell.grid(row = row, column = col, fill = None)

       
        frame.pack(expand = False, fill= None, anchor = "nw", padx = 10, pady = 10)

       

class Controls(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth, rheight, **kwargs):

        #setup control menu
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight,)
    



        #placeholder for visibility of frame
        #ctk.CTkLabel(self, bg_color=colour).pack(expand = True, fill = "both",)


App("Str8ts Solver", (500,500))