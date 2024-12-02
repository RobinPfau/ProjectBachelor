from gridelement import GridElement 

class Converter():
    def __init__(self):
        pass

    def convert(self, puzzlestring):

        if len(puzzlestring) % 2  != 0:
            raise ValueError ("String must be even number of Char")
        if not puzzlestring.isdigit():
            raise ValueError ("String must be only digits")
        
        length = len(puzzlestring) // 2
        intstring = puzzlestring[:length]
        colorstring = puzzlestring[length:]
        puzzle= []

        
        for i in range(length): 
            value = intstring[i]
            color = colorstring[i]
            element = GridElement(int(value), self.colormap.get(color))
            puzzle.append(element)
        return puzzle
    

    @property
    def colormap(self):
        return {"0":"white","1":"black"}
    
             

