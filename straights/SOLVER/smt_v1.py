import cvc5
from cvc5 import Kind

class SmtSolver():
    def __init__(self, matrix, size):

        tm = cvc5.TermManager()
        self.solver = cvc5.Solver()
        self.solver.setOption("produce-models", "true")

        self.matrix_size = size
        self.matrix = matrix

        

    def load_initial_grid(self): 
        initial_grid = []   
        for i in range(self.matrix_size):
            current_row = []
            for j in range (self.matrix_size):
                
                value = self.matrix.grid[i][j].value
                current_row.append(value)
            initial_grid.append(current_row)
        return initial_grid
        

    def find_grid(self):
        
        self.initial_grid = self.load_initial_grid()
        print(self.initial_grid)
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
                    self.solver.assertFormula( self.solver.mkTerm(Kind.DISTINCT, grid[i][j], grid[k][j]))
        

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
            print(solution)
            return solution
        else:
            print("No solution exists that satisfies the constraints.")
            return None