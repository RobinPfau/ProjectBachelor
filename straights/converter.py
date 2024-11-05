from gridelement import GridElement 

class Converter():
    def __init__(self):
        pass

    def convert(self, puzzlestring):
        intstring = puzzlestring[:81]
        colorstring = puzzlestring[81:]
        puzzle= []

        for i in range(len(intstring)): 
            value = intstring[i]
            color = colorstring[i]
            element = GridElement(int(value), self.colormap.get(color))
            puzzle.append(element)
        return puzzle
    

    @property
    def colormap(self):
        return {"0":"white","1":"black"}
    
             

