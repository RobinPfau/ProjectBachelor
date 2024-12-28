import cvc5
from cvc5 import Kind
import random
from .smt_v2 import SmtSolver_v2


class SmtCreator():
    def __init__(self, size = 9):

        self.matrix_size = size
        self.solver = SmtSolver_v2()
        
    def create_colorstring(self):
        black = int((self.matrix_size**2) * 3/9)
        white = (self.matrix_size**2) - black
        colorstring = "1" * black + "0" * white
        color_list = list(colorstring)
        random.shuffle(color_list)
        colorstring = ''.join(color_list)
        colorstring = "100100100000000000001001001110001100000000000001100011100100100000000000001001001"
        return colorstring
    
    
    def create_puzzlestring(self, colorstring):
        intstring = "0" * self.matrix_size**2
        
        #empty = int((self.matrix_size**2) * 7/9)
        full = int((self.matrix_size**2) * 4/9)
        #intstring = "0" * empty
        solver = SmtSolver_v2()
        for i in range(full):
            x = (random.randint(0,8))
            y = (random.randint(0,8))
            print(x,y)
            puzzlestring = intstring + colorstring
            position =  x* self.matrix_size + y
            
            value = str(solver.solve_single(puzzlestring, x, y))
            if value == "None":
                raise ValueError("no value possible")
                
            intstring = intstring[:position] + value + intstring[position+1:]

        #int_list = list(intstring)
        #random.shuffle(int_list)
        return intstring + colorstring
    
    
    def create_puzzle(self): 
        colorstring = self.create_colorstring()
        puzzlestring =  self.create_puzzlestring(colorstring)
        print(puzzlestring)

        puzzlecounter = 0
        while not self.solver.solve(puzzlestring):
            puzzlecounter += 1
            puzzlestring = self.create_puzzlestring(colorstring)
            print(puzzlecounter)
            print(puzzlestring)
    
        return puzzlestring