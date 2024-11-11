import cvc5
from cvc5 import Kind

class SmtSolver():
    def __init__(self, matrix, size):

        tm = cvc5.TermManager()
        self.solver = cvc5.Solver()
        self.solver.setOption("produce-models", "true")

        self.matrix_size = size
        self.matrix = matrix
        print(matrix)


        
    def load_initial_grid(self): 
        initial_grid = []   
        for i in range(self.matrix_size):
            current_row = []

            for j in range (self.matrix_size):
                value = self.matrix.grid[i][j].value
                current_row.append(value)

            initial_grid.append(current_row)

        return initial_grid
    
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
        
        self.initial_grid = self.load_initial_grid()
        print(self.initial_grid)

        straights = self.load_straights()

        int_sort = self.solver.getIntegerSort()       
        grid = [[self.solver.mkConst(int_sort, f"cell_{i}_{j}") for j in range(self.matrix_size)] for i in range(self.matrix_size)]
        

        for i in range (self.matrix_size):
            for j in range (self.matrix_size):
                # Constraint: given values must be constant
                if self.initial_grid[i][j] != 0:

                    self.solver.assertFormula(self.solver.mkTerm(Kind.EQUAL, grid[i][j], self.solver.mkInteger(self.initial_grid[i][j])))
                else:
                    # Constraint: each cell must be greater or equal than 1
                    self.solver.assertFormula(self.solver.mkTerm(Kind.GEQ, grid[i][j], self.solver.mkInteger(1)))
                    # Constraint: each cell must be less or equal than 9
                    self.solver.assertFormula(self.solver.mkTerm(Kind.LEQ, grid[i][j], self.solver.mkInteger(9)))


        #positive cells
        # for i in range(self.matrix_size):
        #    for j in range(self.matrix_size):
        #        # Constraint: each cell must be greater or equal to
        #        self.solver.assertFormula(self.solver.mkTerm(Kind.GEQ, grid[i][j], self.solver.mkInteger(1)))


        #distinct values in rows
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                for k in range(j + 1, self.matrix_size):
                    # Constraint: each cell must be distinct in its row:
                    self.solver.assertFormula(self.solver.mkTerm(Kind.DISTINCT, grid[i][j], grid[i][k]))


        #distinct values in col
        for j in range( self.matrix_size):
            for i in range( self.matrix_size):
                for k in range(i + 1,  self.matrix_size):
                    # Constraint: each cell must be distinct in its column:
                    self.solver.assertFormula(self.solver.mkTerm(Kind.DISTINCT, grid[i][j], grid[k][j]))


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

            for tupel in element:
                i = tupel[0]
                j = tupel[1]
                cells_in_straight.append(grid[i][j])
            
          
            max_integer_const = cells_in_straight[0]
            min_integer_const = cells_in_straight[0]

            for integer_const in cells_in_straight[1:]:
               
                max_integer_const = self.solver.mkTerm(Kind.ITE, self.solver.mkTerm(Kind.GT, max_integer_const, integer_const), max_integer_const, integer_const)                                     
                min_integer_const = self.solver.mkTerm(Kind.ITE, self.solver.mkTerm(Kind.LT, integer_const, min_integer_const), integer_const, min_integer_const)          
            
            difference = self.solver.mkInteger(len(cells_in_straight)-1)
            print(difference)

            diff_term = self.solver.mkTerm(Kind.SUB, max_integer_const, min_integer_const)

            self.solver.assertFormula(self.solver.mkTerm(Kind.EQUAL, diff_term, difference))

            #self.solver.assertFormula(self.solver.mkTerm(Kind.EQUAL, min_integer_const, self.solver.mkTerm(Kind.SUB, max_integer_const, difference)))


                # Constraint: Minimum in straight = maximum - n -1
                #self.solver.assertFormula(self.solver.mkTerm(Kind.EQUAL, MAximum, minum -n-1)
  

        if self.solver.checkSat().isSat():
            print("Solution found:")
            solution = []
            for i in range(self.matrix_size):
                row = []
                for j in range(self.matrix_size):
                    # Get the model value for each cell in the grid
                    
                    cell_value = self.solver.getValue(grid[i][j]).getIntegerValue()
                    
                    row.append(cell_value)
                solution.append(row)
           
            return solution
        else:
            print("No solution exists that satisfies the constraints.")
            return None