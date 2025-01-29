import random
import math
from .smt_v3 import SmtSolver_v3

class SmtCreator():
    def __init__(self, parent):
        self.parent = parent
        self.solver = SmtSolver_v3()
        self.intstring = None
        self.reset_intstring()
    
    @property
    def difficulty_map(self):
        return {
                "easy": {"n_black": 25, "n_int": 23},
                "medium": {"n_black": 22, "n_int": 19},
                "hard": {"n_black": 22, "n_int": 13},
                "impossible": { "n_black": 21, "n_int": 12}
                }

    def create_seed(self, size, symmetry, difficulty):
        """
        Creates a new puzzleboard
        """
        n_black = self.difficulty_map[difficulty]["n_black"]
        n_white = 81 - n_black
        if symmetry == "symmetric":
            n_black = n_black//2
            n_white = 40 - n_black

        black = "1" * n_black
        white = "0" * n_white
        stringlist = list(black + white)
        random.shuffle(stringlist)
        #creates symmetric board

        colorstring = "".join(stringlist)
        if symmetry == "symmetric":
            colorstring_two = colorstring[::-1]
            fill = str(random.choice([0,1]))
            colorstring = colorstring + fill + colorstring_two

        #print(colorstring)
        
        return colorstring
    
    def fill_seed(self, size):

        colorlist = list(self.colorstring)
        intlist = list(self.intstring)
        for _ in range(random.choice([5,6])):

            non_zero_indices = [i for i, color in enumerate(colorlist) if color == "1" and intlist[i] == "0"]
            index = random.choice(non_zero_indices)
            value = random.choice([1,2,3,4,5,6,7,8,9])
            #print(value)
            
            temp_intstring = "".join(intlist)
            intlist[index] = str(value)

            if self.check_start_value(temp_intstring, size, index//9, index%9, value):
                print("found non unique start value at index: ", index)
                intlist[index] = "0"
                   
        self.intstring = "".join(intlist)
        #print(self.intstring + self.colorstring)
        return self.intstring + self.colorstring
    


    def create_puzzle(self, size, symmetry, difficulty):
        """
        kekw
        """
        
        self.colorstring = self.create_seed(size, symmetry, difficulty)

        self.matrix_size = math.sqrt(len(self.colorstring))

        puzzlestring = self.fill_seed(size)

        print(f"creating a {difficulty} {symmetry} puzzle")
       
        solutions = self.solver.solve(puzzlestring)
        counter = 0
        while not solutions:
            
            print(f"failed attempt: #{counter}")
            self.parent.display.update_display("attempt failed")
            self.reset_intstring()
            self.colorstring = self.create_seed(size, symmetry, difficulty)
            puzzlestring = self.fill_seed(size)
            #print( puzzlestring)
            solutions = self.solver.solve(puzzlestring)
            counter += 1

        self.save_solution(solutions)

        puzzlestring = self.intstring + self.colorstring
        solutions = self.solver.solve(puzzlestring)
        print(self.solver.alternate_solution())


        for attempt in range(5):
            print("this is reduce try number :", attempt + 1)
            n_int = self.difficulty_map[difficulty]["n_int"]
            while len([i for i, value in enumerate(self.intstring) if value != "0"]) > n_int:

                reduced_intstring = self.reduce_solution()
            
                puzzlestring =  reduced_intstring + self.colorstring
                solutions = self.solver.solve(puzzlestring)
                if self.solver.alternate_solution():
                    print("found alternate, restarting loop")
                    break

                self.intstring = reduced_intstring  

        print("found non unique")
        print(self.intstring + self.colorstring)
        self.parent.display.update_display(f"created {difficulty} {symmetry}")
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

        non_zero_indices = [i for i, value in enumerate(stringlist) if value != "0" and self.colorstring[i] == "0"]
            
        #indices = random.sample(range(len(stringlist)), 2)
        index = random.choice(non_zero_indices)

        #for index in indices:
        stringlist[index] = "0"

        reduced_intstring = "".join(stringlist)
        return reduced_intstring
    
    def reset_intstring(self):
        self.intstring = "000000000000000000000000000000000000000000000000000000000000000000000000000000000"

    def check_start_value(self, intstring:str, size:int, x:int, y:int, value:int) -> bool:
        col = [intstring[i*size + y] for i in range(size)]
        row = [intstring[y*size + x] for x in range(size)]
        return str(value) in col or str(value) in row