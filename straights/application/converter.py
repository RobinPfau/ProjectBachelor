from .gridelement import GridElement 

class Converter():
    def __init__(self):
        pass
    #converts a puzzlestring into a list of GridElements
    def convert(self, puzzlestring):
        #check if string is even
        if len(puzzlestring) % 2  != 0:
            raise ValueError ("String must be even number of Char")
        #check if string is only digits
        if not puzzlestring.isdigit():
            raise ValueError ("String must be only digits")
        
        length = len(puzzlestring) // 2     
        intstring = puzzlestring[:length]   #string of the values
        colorstring = puzzlestring[length:] #string of the colors
        puzzle= []

        #create GridElements
        for i in range(length): 
            value = intstring[i]
            color = colorstring[i]
            element = GridElement(int(value), self.colormap.get(color))
            puzzle.append(element)
        
        return puzzle
    
    #mapping for the colors
    @property
    def colormap(self):
        return {"0":"white","1":"black"}
    
             

