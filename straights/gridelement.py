class GridElement():
    def __init__(self, value: int = 0 , color: str = "White"):
        self.value = value
        self.color = color

    def get_text_color(self):
        if self.value == 0 and self.color == "white":
            return "blue"
        elif self.value != 0 and self.color == "white":
            return "black"
        return "white"
    
    def get_state(self):
        if self.value == 0 and self.color == "white":
            
            return "normal"
        else:
            return "disabled" 
            print("wiso nix normal")


            