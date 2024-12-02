import math
import cvc5
from cvc5 import Kind

# Class definition for the SMT cvc5 puzzle solver Version2
class SmtSolver_v2():
    def __init__(self):

        self.solver = cvc5.Solver()

        self.solver.setOption("produce-models", "true")
        # self.solver.setOption("decision-stategy", "value")
        #self.solver.setOption("time-limit", "10000")

        self.int_sort = self.solver.getIntegerSort()   
        self.bool_sort = self.solver.getBooleanSort()

        
    def setup(self, puzzlestring):
        # Extract the puzzle configuration from the given string
                
        midpoint = int((len(puzzlestring)) // 2)
        self.matrix_size = int(math.sqrt(midpoint))
       
        # Separate the integer values and color indicators from the input string
        self.intstring = puzzlestring[:midpoint]
        self.colorstring = puzzlestring[midpoint:]

        # Create matrix of symbolic integers
        self.value_matrix = [[self.solver.mkConst(self.int_sort, f"value_{x}_{y}")
                                for x in range(self.matrix_size)] 
                                for y in range(self.matrix_size)]
        # create matrix of symbolic booleans
        self.color_matrix = [[self.solver.mkConst(self.bool_sort, f"color_{x}_{y}")
                                for x in range(self.matrix_size)]
                                for y in range(self.matrix_size)]
             

    def value_rule(self):
        # Define constraints based on puzzle rules for value and color
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                # Get the value and color of the current cell from the input
                value = int(self.intstring[x * self.matrix_size + y])
                black = True if int(self.colorstring[x * self.matrix_size + y]) == 1 else False

                # Constraint for the color of the cell
                color_constraint = self.solver.mkTerm(Kind.EQUAL,
                                                      self.color_matrix[x][y],  
                                                      self.solver.mkBoolean(black))
                self.solver.assertFormula(color_constraint)
                #print(color_constraint)

                # Constraints for the value based on its color and given value
                if value != 0:  # If a fixed value is provided
                    value_constraint = self.solver.mkTerm(
                        Kind.EQUAL, 
                        self.value_matrix[x][y],  
                        self.solver.mkInteger(value))
                
                elif black:  # If the cell is black, its value must be ≤ -1
                    value_constraint = self.solver.mkTerm(
                        Kind.LEQ,
                        self.value_matrix[x][y],
                        self.solver.mkInteger(-1))
                    
                else:  # If the cell is white, its value must be in the valid range
                    value_constraint = (self.solver.mkTerm(Kind.AND, 
                                                                self.solver.mkTerm(
                                                                    Kind.GEQ,
                                                                    self.value_matrix[x][y],
                                                                    self.solver.mkInteger(1)),
                                                                self.solver.mkTerm(
                                                                    Kind.LEQ,
                                                                    self.value_matrix[x][y],
                                                                    self.solver.mkInteger(self.matrix_size))))
                # Add the value constraint to the list of constraints
                self.solver.assertFormula(value_constraint)
                print(value_constraint, color_constraint)

    def unique_rule(self):
               
        for x in range(self.matrix_size):
            # Ensure all values in each row are distinct
            col = [self.value_matrix[x][y] for y in range(self.matrix_size)]
            unique_col_constraint = self.solver.mkTerm(Kind.DISTINCT, *col)
            self.solver.assertFormula(unique_col_constraint)
            print(unique_col_constraint)
            

        for y in range(self.matrix_size):
            # Ensure all values in each column are distinct
            row = [self.value_matrix[x][y] for x in range(self.matrix_size)]
            unique_row_constraint = self.solver.mkTerm(Kind.DISTINCT, *row)
            self.solver.assertFormula(unique_row_constraint)
            print(unique_row_constraint)


    def consecutive_rule(self):
        # Enforce consecutive constraints for sequences of white cells in rows and columns
        
        # Check consecutive sequences in rows
        for x in range(self.matrix_size):
            straight = []  # List to track consecutive white cells

            for y in range(self.matrix_size):
                # Check if the cell is black or white
                black = True if int(self.colorstring[x * self.matrix_size + y]) == 1 else False

                if not black:  # White cell, add to the current sequence
                    straight.append(self.value_matrix[x][y])
                else:  # Black cell, enforce consecutive rule for the sequence
                    if 1 < len(straight) < self.matrix_size:
                        self.enforce_consecutive(straight, "row", x)
                    straight = []

            if 1 < len(straight) < self.matrix_size:  # Check the last sequence in the row
                self.enforce_consecutive(straight, "row", x)

        # Check consecutive sequences in columns
        for y in range(self.matrix_size):
            straight = []  # List to track consecutive white cells

            for x in range(self.matrix_size):
                # Check if the cell is black or white
                black = True if int(self.colorstring[x * self.matrix_size + y]) == 1 else False

                if not black:  # White cell, add to the current sequence
                    straight.append(self.value_matrix[x][y])
                else:  # Black cell, enforce consecutive rule for the sequence
                    if 1 < len(straight) < self.matrix_size:
                        self.enforce_consecutive(straight, "col", y)
                    straight = []

            if 1 < len(straight) < self.matrix_size:  # Check the last sequence in the column
                self.enforce_consecutive(straight, "col", y)


    def enforce_consecutive(self, straight, name, coord):
        # Add constraints to ensure values in a sequence are consecutive

        # Define variables for the minimum and maximum of the sequence
        min_value = self.solver.mkConst(self.int_sort, f"min_{name}_{coord}")
        max_value = self.solver.mkConst(self.int_sort, f"max_{name}_{coord}")

        # Constraints to bind min and max to the sequence values
        min_constraint = [self.solver.mkTerm(Kind.LEQ, min_value, value) for value in straight]
        max_constraint = [self.solver.mkTerm(Kind.GEQ, max_value, value) for value in straight]
        
        # Constraint to enforce the range of values
        range_constraint = self.solver.mkTerm(
            Kind.EQUAL,
            self.solver.mkTerm(Kind.SUB, max_value, min_value), 
            self.solver.mkInteger(len(straight) - 1)
        )
        
        # Combine all constraints for the sequence
        consecutive_constraint = min_constraint + max_constraint + [range_constraint]

        # Enforce the constraints together
        straight_constraint = self.solver.mkTerm(Kind.AND, *consecutive_constraint)
        self.solver.assertFormula(straight_constraint)
        print(straight_constraint)


    def solve(self, puzzlestring):
        # Main method to solve the puzzle
        
        self.setup(puzzlestring)  # Setup the matrices and initial constraints
        self.value_rule()  # Apply value-based rules
        self.unique_rule()  # Apply uniqueness rules
        self.consecutive_rule()  # Apply consecutive rules  
            
        # Check and return the solution
        return self.check_solution()
      
    def check_solution(self):
        # Check satisfiability and extract the solution if one exists
        
        if self.solver.checkSat().isSat():
            print("Solution found:")
            solution = []
            for x in range(self.matrix_size):
                row = []
                for y in range(self.matrix_size):
                    # Get the value of each cell
                    cell_value = self.solver.getValue(self.value_matrix[x][y]).getIntegerValue()

                    if cell_value > 0:  # Only positive values are part of the solution
                        row.append(cell_value)
                    else:
                        row.append(0)  # Black cells have a value of 0
                print(row)  # Print the solution row
                solution.append(row)
            
            return solution
        else:
            print("No solution exists that satisfies the constraints.")
            return None


    def alternate_solution(self):
        # Check if another solution exists
        if not self.solver.checkSat().isSat():
            print("no solution in the first place when checking for multiple")
            return False, None
        
        current_solution = []
        for x in range(self.matrix_size):
            row = []
            for y in range(self.matrix_size):
            
                value = self.solver.getValue(self.value_matrix[x][y]).getIntegerValue()
                row.append(value)
            current_solution.append(row)

        different_constraints = []
        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                current_value = current_solution[x][y] 
                if current_value < 0:
                    continue

                different_constraint = self.solver.mkTerm(
                                                        Kind.DISTINCT,
                                                        self.value_matrix[x][y],
                                                        self.solver.mkInteger(current_value)
                                                        )
                different_constraints.append(different_constraint)

        if not different_constraints:
            print("No non-black cells to change, cannot find an alternate solution.")
            return False, None

        alternate_solution_constraint = self.solver.mkTerm(Kind.OR, *different_constraints)
        self.solver.push()
        self.solver.assertFormula(alternate_solution_constraint)

        alternate = self.solver.checkSat().isSat()

        if alternate:
            print("Another solution exists.")
            alternate_solution = []
            for x in range(self.matrix_size):
                row = []
                for y in range(self.matrix_size):
                # Get the integer value of each cell in the alternate solution
                    value = self.solver.getValue(self.value_matrix[x][y]).getIntegerValue()
                    if value > 0:
                        row.append(value)
                    else:
                        row.append(0)
                alternate_solution.append(row)
        
            # Print the alternate solution
            for row in alternate_solution:
                print(row)            
        else:
            print("No other solution exists.")

        self.solver.pop()

        return alternate, alternate_solution if alternate else None

     
    def unique_single_rule(self,row,col):
  
        row_list = [self.value_matrix[row][y] for y in range(self.matrix_size)]
        unique_row_constraint = self.solver.mkTerm(Kind.DISTINCT, *row_list)
        self.solver.assertFormula(unique_row_constraint)
        print(unique_row_constraint)

        column_list = [self.value_matrix[x][col] for x in range(self.matrix_size)]
        unique_col_constraint = self.solver.mkTerm(Kind.DISTINCT, *column_list)
        self.solver.assertFormula(unique_col_constraint)
        print(unique_col_constraint)


    def consecutive_single_rule(self, row, col):
        #black cell -> no straights
        if int(self.colorstring[row * self.matrix_size + col]) == 1:
                return
        
        straight = []    
        for y in range(self.matrix_size):   
            black = True if int(self.colorstring[row * self.matrix_size + y]) == 1 else False

            if not black:
                straight.append(self.value_matrix[row][y])
            else:
                if len(straight) > 1: 
                    self.enforce_consecutive(straight, row)
    
        if len(straight) > 1: 
            self.enforce_consecutive(straight, row)
            straight = []

        straight = []  

        for x in range(self.matrix_size):        
            black = True if int(self.colorstring[x * self.matrix_size + col]) == 1 else False

            if not black: 
                straight.append(self.value_matrix[x][col])
            else: 
                if len(straight) > 1: 
                    self.enforce_consecutive(straight, col)

        if len(straight) > 1: 
            self.enforce_consecutive(straight, col)



    def solve_single(self, puzzlestring, x, y):

        self.setup(puzzlestring)
        self.value_rule()
        self.unique_single_rule(x,y)
        self.consecutive_single_rule(x,y)
               
        if self.solver.checkSat().isSat():
            print("Single solution found:")
            cell_value = self.solver.getValue(self.value_matrix[x][y]).getIntegerValue()
            print(cell_value)
            if cell_value < 1:
                return 0
            return cell_value
        else:
            print("no cell value possible")
           
