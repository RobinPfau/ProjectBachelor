import customtkinter as ctk
from .matrix import Matrix
from .cell import Cell

class Grid(ctk.CTkFrame):
    
    def __init__(self, parent, x, y, colour, rwidth,  rheight, matrix: Matrix, **kwargs):
        
        #setup frame
        super().__init__(parent, **kwargs)
        self.place(relx = x, rely= y, relwidth = rwidth, relheight = rheight)
        self.selected_cell = None
        self.matrix = matrix
        self.create_grid()
        
    def delete_grid(self):
        self.frame.destroy()


    def create_grid(self):
        #puzzle frame
        self.frame = ctk.CTkFrame(self)
                
        for row in range(9):
            rowlist = self.matrix.grid[row]
            self.frame.grid_rowconfigure(row, weight=1)
        
            for col in range(9):
                self.frame.grid_columnconfigure(col, weight=1)
                
                border_frame = ctk.CTkFrame(self.frame, fg_color = "white")
                border_frame.grid(row=row, column=col, fill = None )          
                
                cell = Cell(border_frame, xcoord = row, ycoord = col, width = 70, height = 70, font = ("Arial", 50),justify = "center",)

                #bind functionality to the cells
                cell.bind("<FocusIn>", lambda event, frame=border_frame, cell = cell: self.on_click_in(event, frame, cell))
                cell.bind("<FocusOut>", lambda event, frame=border_frame: self.on_click_out(event, frame))
                cell.bind("<KeyRelease-BackSpace>", self.on_delete)
                cell.bind("<KeyRelease-Delete>", self.on_delete)
                cell.bind("<KeyRelease>", self.on_entry)

                content = rowlist[col]
                if content.value != 0:
                    cell.insert(0, content.value)
                cell.configure(fg_color = content.color, text_color = content.get_text_color(), state = content.get_state())
                
                cell.pack(padx = 1,pady = 1)
                #cell.grid(row = row, column = col, fill = None,) 
                
  
        self.frame.pack(expand = False, fill= None, anchor = "nw", padx = 20, pady = 20)
    
    
    #select entry with mouse, indicate visually
    def on_click_in(self, event, frame, cell):
        frame.configure(fg_color = "lightgreen")
        self.selected_cell = cell


    #needed for losing focus 
    def on_click_out(self, event, frame):
        frame.configure(fg_color = "white")


    #functionality on typing in cell, update visual and matrix
    def on_entry(self, event):
        cell = event.widget
        
        x = self.selected_cell.x
        y = self.selected_cell.y

        if cell.get():
            current_value = cell.get()[0]
            cell.delete(0, "end")
            if event.char.isdigit() and event.char != "0":
                cell.insert(0, event.char)
                self.matrix.grid[x][y].value = int(event.char)
                #print(self.matrix.grid[x][y])
                print(self.matrix.grid[x][y].value)

            elif current_value in "123456789":
                cell. insert(0, current_value)

    def on_delete(self, event):
        x = self.selected_cell.x
        y = self.selected_cell.y
       
        if self.matrix.grid[x][y].value == 0:
            return
        
        cell = event.widget
        cell.delete(0, "end")
      
        self.matrix.grid[x][y].value = 0
        print(self.matrix.grid[x][y].value)
        print("löscher")
        # enter the value into backend
        #print(event.char)    