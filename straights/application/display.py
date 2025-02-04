import customtkinter as ctk

class Display(ctk.CTkFrame):
    def __init__(self, parent, start_text, x, y, relw, relh, **kwargs):
        
        super().__init__(parent, **kwargs)
        #create display
        self.display = ctk.CTkLabel(self, text = start_text, font=("Arial", 20), fg_color="gray20")
        #place display
        self.display.place(relx=0, rely=0, relwidth=1, relheight=1) 
        self.place(relx = x, rely =y, relwidth = relw, relheight = relh)
    
    #updates the text shown in the display
    def update_display(self, new_text:str):
        self.display.configure(text = new_text)
    