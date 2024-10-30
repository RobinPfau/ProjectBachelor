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

        #widgets
        self.frame1 = Frame(self, 0, 0, "green", 0.65, 1)
        self.frame1 = Frame(self, 0.7, 0, "red", 0.3, 1)
        #run
        self.mainloop()

class Frame(ctk.CTkFrame):
    def __init__(self, parent, x, y, colour, rwidth,  rheight, **kwargs):
        
        #setup frame
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight,)
        ctk.CTkLabel(self, bg_color=colour).pack(expand = True, fill = "both",)


App("Str8ts Solver", (500,500))