import cvc5
from cvc5 import Kind

class SmtSolver():
    def __init__(self, puzzle, matrix, size):

        self.solver = cvc5.Solver()
        self.solver.setOption("produce-models", "true")

        self.matrix_size = size
        self.matrix = matrix
        self.intstring = puzzle[:81]
        self.colorstring = puzzle[81:]

    
        #for i in range(self.matrix_size):
       #     current_row = []

       #     for j in range (self.matrix_size):
        #        value = self.matrix.grid[i][j].value
         #       current_row.append(value)

          #  initial_grid.append(current_row)

       # return initial_grid
    
    def load_straights(self):
        straightlist = []
        for list in self.matrix.straights:
            straight = []

            for element in list:
                cell = (element.x, element.y)
                straight.append(cell)
               
            straightlist.append(straight)

    
        return straightlist
        

    def find_grid(self):
        
        straights = self.load_straights()
        int_sort = self.solver.getIntegerSort()    

        grid = [[self.solver.mkConst(int_sort, f"cell_{x}_{y}") for x in range(self.matrix_size)] for y in range(self.matrix_size)]
        counter = 0    

        for x in range (self.matrix_size):
            for y in range (self.matrix_size):
                value = int(self.intstring[counter])
                color = int(self.colorstring[counter])
                # Constraint: given values must be constant
                if value != 0:
                    self.solver.assertFormula(self.solver.mkTerm(Kind.EQUAL, grid[x][y], self.solver.mkInteger(value)))
                # Constraint: empty black values must be ignored
                elif color == 1:
                    self.solver.assertFormula(self.solver.mkTerm(Kind.LEQ,  grid[x][y], self.solver.mkInteger(-1)))
                else:    
                    # Constraint: each cell must be greater or equal than 1
                    self.solver.assertFormula(self.solver.mkTerm(Kind.GEQ, grid[x][y], self.solver.mkInteger(1)))
                    # Constraint: each cell must be less or equal than 9
                    self.solver.assertFormula(self.solver.mkTerm(Kind.LEQ, grid[x][y], self.solver.mkInteger(9)))
                counter += 1

        #positive cells
        # for i in range(self.matrix_size):
        #    for j in range(self.matrix_size):
        #        # Constraint: each cell must be greater or equal to
        #        self.solver.assertFormula(self.solver.mkTerm(Kind.GEQ, grid[i][j], self.solver.mkInteger(1)))


        #distinct values in rows
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                for k in range(y + 1, self.matrix_size):
                    # Constraint: each cell must be distinct in its row:
                    self.solver.assertFormula(self.solver.mkTerm(Kind.DISTINCT, grid[x][y], grid[x][k]))


        #distinct values in col
        for y in range( self.matrix_size):
            for x in range( self.matrix_size):
                for k in range(x + 1,  self.matrix_size):
                    # Constraint: each cell must be distinct in its column:
                    self.solver.assertFormula(self.solver.mkTerm(Kind.DISTINCT, grid[x][y], grid[k][y]))


        #values in straights are consecutive
              #minimum in straight = maximum in straight - (n-1)
       # for j in range( self.matrix_size):
        #    for i in range( self.matrix_size):
         #      
          #      for element in straights:
           #         for tupel in element:
            #            if tupel[0] == i and tupel[1] == j:
             #               for tupel in element 
              #              
               #             self.solver.mkTerm(Kind))


        
        for element in straights:
           
            cells_in_straight = []
            print(element)
            for tupel in element:
                x = tupel[0]
                y = tupel[1]
                cells_in_straight.append(grid[x][y])
            
          
            max_integer_const = cells_in_straight[0]
            min_integer_const = cells_in_straight[0]

            for integer_const in cells_in_straight[1:]:
               
                max_integer_const = self.solver.mkTerm(Kind.ITE, self.solver.mkTerm(Kind.GT, max_integer_const, integer_const), max_integer_const, integer_const)                                     
                min_integer_const = self.solver.mkTerm(Kind.ITE, self.solver.mkTerm(Kind.LT, min_integer_const, integer_const), min_integer_const, integer_const)          
            
            difference = self.solver.mkInteger(len(cells_in_straight) - 1)
            
            diff_term = self.solver.mkTerm(Kind.SUB, max_integer_const, min_integer_const)

            self.solver.assertFormula(self.solver.mkTerm(Kind.EQUAL, diff_term, difference))

            #self.solver.assertFormula(self.solver.mkTerm(Kind.EQUAL, min_integer_const, self.solver.mkTerm(Kind.SUB, max_integer_const, difference)))


                # Constraint: Minimum in straight = maximum - n -1
                #self.solver.assertFormula(self.solver.mkTerm(Kind.EQUAL, MAximum, minum -n-1)
  

        if self.solver.checkSat().isSat():
            print("Solution found:")
            solution = []
            for x in range(self.matrix_size):
                row = []
                for y in range(self.matrix_size):
                    # Get the model value for each cell in the grid
                    cell_value = self.solver.getValue(grid[x][y]).getIntegerValue()
                    row.append(cell_value)

                solution.append(row)
            print(solution)
            return solution
        else:
            print("No solution exists that satisfies the constraints.")
            return None