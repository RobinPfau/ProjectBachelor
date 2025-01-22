import random
import math
from .smt_v3 import SmtSolver_v3

class SmtCreator():
    def __init__(self, parent):
        self.parent = parent
        self.solver = SmtSolver_v3()
        self.intstring = "000000000000000000000000000000000000000000000000000000000000000000000000000000000"


    def create_seed(self, size):
        """
        Creates a new puzzleboard
        """

        ones = "1" * 11
        os = "0" * 29
        stringlist = list(ones + os)
        random.shuffle(stringlist)
        #creates symmetric board
        colorstring_one = "".join(stringlist)
        colorstring_two = colorstring_one[::-1]
        colorstring = colorstring_one  + "0" + colorstring_two

        print(colorstring)
        
        return colorstring

    def create_puzzle(self, size):
        
        self.colorstring = self.create_seed(size)
        self.matrix_size = math.sqrt(len(self.colorstring))
        puzzlestring = self.intstring + self.colorstring
       
        print(puzzlestring)
        print("creating a puzzle")
       
        

        #for filler in range(4):
        #    intlist = list(self.)

        solutions = self.solver.solve(puzzlestring)
        self.save_solution(solutions)

        puzzlestring = self.intstring + self.colorstring
        solutions = self.solver.solve(puzzlestring)
        print(self.solver.alternate_solution())


        for attempt in range(8):
            print("this is reduce try number :", attempt + 1)
           
            while True:
                checkpoint = self.intstring
                self.reduce_solution()
            
                puzzlestring = self.intstring + self.colorstring
                solutions = self.solver.solve(puzzlestring)
                if self.solver.alternate_solution():
                    self.intstring = checkpoint
                    print("found alternate, restarting loop")
                    break
                
        print("found non unique")
        print(self.intstring + self.colorstring)
        return self.intstring + self.colorstring
               

    def save_solution(self, solutions):

        for x, row in enumerate(solutions):
            for y, solution in enumerate(row):
                if solution > 0:
                   index = x*9+y
                   stringlist = list(self.intstring)
                   stringlist[index] = str(solution)
                   self.intstring = "".join(stringlist)
        print("saved solution: ", self.intstring)

    def reduce_solution(self):
        stringlist = list(self.intstring)

        non_zero_indices = [i for i, value in enumerate(stringlist) if value != "0"]
        #indices = random.sample(range(len(stringlist)), 2)
        index = random.choice(non_zero_indices)

        #for index in indices:
        stringlist[index] = "0"

        self.intstring = "".join(stringlist)