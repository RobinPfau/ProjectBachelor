 
class GridElement():
    def __init__(self, value: int = 0 , color: str = "white", x: int = 0, y: int = 0):
        self.value = value
        self.color = color
        self.x = x
        self.y = y
        self.solution = None
    
    #get the color of the cell
    def get_text_color(self):
        if self.value == 0 and self.color == "white":
            return "blue"
        elif self.value != 0 and self.color == "white":
            return "black"
        return "white"
    
    #get the interctive state of the cell
    def get_state(self):
        if self.color == "white":
            if self.value == 0:
                return "normal"
            else:
                return "readonly"
        else:
            return "disabled"