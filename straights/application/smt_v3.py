import math
import cvc5
from cvc5 import Kind
import time

# Class definition for the SMT cvc5 puzzle solver Version2
class SmtSolver_v3():
    def __init__(self):

        self.solver = cvc5.Solver()

        self.solver.setOption("produce-models", "true")
        self.solver.setOption("verbosity", "0")
        self.solver.setOption("stats", "true")
        #self.solver.setOption("stats-every-query", "true")
        self.solver.setOption("output", "portfolio")
        #self.solver.setOption("output", "trigger")
        self.solver.setOption("produce-proofs", "true")
        self.solver.getStatistics()

        #solver logic integer difference logic
        #self.solver.setLogic("QF_IDL")
        #solver logig linear integer algebra
        self.solver.setLogic("QF_LIA")

        #schämecke
        # self.solver.setOption("threads", "4")
        # self.solver.setOption("decision-stategy", "value")
        # self.solver.setOption("time-limit", "10000")

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
               

                # Constraints for the value based on its color and given value
                if value != 0:  # If a fixed value is provided
                    value_constraint = self.solver.mkTerm(
                        Kind.EQUAL, 
                        self.value_matrix[x][y],  
                        self.solver.mkInteger(value))
                
                elif black:  # If the cell is black, its value is set to < 0 (ignored)
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
                #print(value_constraint, color_constraint)


    def unique_rule(self):
               
        for x in range(self.matrix_size):
            # Ensure all values in each row are distinct
            col = [self.value_matrix[x][y] for y in range(self.matrix_size) if not(self.find_color(x,y) == 1 and self.find_value(x,y) == 0)]
            if len(col) > 1:
                unique_col_constraint = self.solver.mkTerm(Kind.DISTINCT, *col)
                self.solver.assertFormula(unique_col_constraint)
                #print(unique_col_constraint)
            

        for y in range(self.matrix_size):
            # Ensure all values in each column are distinct
            row = [self.value_matrix[x][y] for x in range(self.matrix_size) if not(self.find_color(x,y) == 1 and self.find_value(x,y) == 0)]
            if len(row) > 1:
                unique_row_constraint = self.solver.mkTerm(Kind.DISTINCT, *row)
                self.solver.assertFormula(unique_row_constraint)
                #print(unique_row_constraint)


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
        #print(straight_constraint)


    def solve_stepwise(self):
        self.solver.push()
        # Main method to solve the puzzle

        starttime = time.time()

        self.value_rule()  # Apply value-based rules
        if self.solver.checkSat().isSat():
            print(f"Solving value took {time.time() - starttime} seconds.")
        starttime = time.time()
        
        self.consecutive_rule()  # Apply consecutive rules  
        if self.solver.checkSat().isSat():
            print(f"Solving consecutive took {time.time() - starttime} seconds.")
        self.unique_rule()  # Apply uniqueness rules
        if self.solver.checkSat().isSat():
            print(f"Solving unique took {time.time() - starttime} seconds.")
        starttime = time.time()

        self.solver.pop()


    def solve(self, puzzlestring):
        print(puzzlestring)
        self.solver.resetAssertions()
        self.setup(puzzlestring)  # Setup the matrices and initial constraints

        #self.solve_stepwise()

        self.value_rule()  # Apply value-based rules
        self.unique_rule()  # Apply uniqueness rules
        self.consecutive_rule()  # Apply consecutive rules  

        # Check and return the solution
        return self.check_solution()
      
    def check_solution(self):
        # Check satisfiability and extract the solution if one exists
        starttime = time.time()
        if self.solver.checkSat().isSat():
            print(f"Solving the puzzle took {time.time() - starttime} seconds.")
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
                #print(row)  # Print the solution row
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

        return alternate #alternate_solution if alternate else None


 #
 #___________________________ single rules _________________________________  
 # 
    
    def unique_single_rule(self,row,col):
  
        row_list = [self.value_matrix[row][y] for y in range(self.matrix_size)]
        unique_row_constraint = self.solver.mkTerm(Kind.DISTINCT, *row_list)
        self.solver.assertFormula(unique_row_constraint)
        #print(unique_row_constraint)

        column_list = [self.value_matrix[x][col] for x in range(self.matrix_size)]
        unique_col_constraint = self.solver.mkTerm(Kind.DISTINCT, *column_list)
        self.solver.assertFormula(unique_col_constraint)
        #print(unique_col_constraint)


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
                    self.enforce_consecutive(straight, "row", row)
    
        if len(straight) > 1: 
            self.enforce_consecutive(straight, "row", row)
            straight = []

        straight = []  

        for x in range(self.matrix_size):        
            black = True if int(self.colorstring[x * self.matrix_size + col]) == 1 else False

            if not black: 
                straight.append(self.value_matrix[x][col])
            else: 
                if len(straight) > 1: 
                    self.enforce_consecutive(straight, "col", col)

        if len(straight) > 1: 
            self.enforce_consecutive(straight, "col", col)



    def straight_single_rule(self, row, col):

        straight = []       
        for y in range(col, -1, -1):   
            black = True if int(self.colorstring[row * self.matrix_size + y]) == 1 else False

            if not black:
                straight.append(self.value_matrix[row][y])
            else:
               break
        
        for y in range(col + 1, self.matrix_size):   
            black = True if int(self.colorstring[row * self.matrix_size + y]) == 1 else False

            if not black:
                straight.append(self.value_matrix[row][y])
            else:
               break

        if len(straight) > 1:
            self.enforce_consecutive(straight, "row", row)
            #print(f"straight in row {row} of lentgh {len(straight)}")


        straight = []
        for x in range(row, -1, -1):   
            black = True if int(self.colorstring[x * self.matrix_size + col]) == 1 else False

            if not black:
                straight.append(self.value_matrix[x][col])
            else:
               break
        
        for x in range(row + 1, self.matrix_size):   
            black = True if int(self.colorstring[x * self.matrix_size + col]) == 1 else False

            if not black:
                straight.append(self.value_matrix[x][col])
            else:
               break
            
        if len(straight) > 1:
            self.enforce_consecutive(straight, "col", col)
           #print(f"straight in col {col} of lentgh {len(straight)}")

    #relic from creatorv2
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


    def find_next_cells(self, puzzlestring):

        possibilities = {}

        self.setup(puzzlestring)
        self.value_rule()

        for x in range(self.matrix_size):
            for y in range(self.matrix_size):
                possible_values = []

                for value in range (1,self.matrix_size):
                    temp_constraint = self.solver.mkTerm(
                        Kind.EQUAL,
                        self.value_matrix[x][y],
                        self.solver.mkInteger(value)
                    )
                    self.solver.push()
                    self.solver.assertFormula(temp_constraint)

                    if self.solver.checkSat().isSat():
                        possible_values.append(value)
                    
                    self.solver.pop()
                    
                if possible_values:
                    possibilities[(x, y)] = possible_values

    #functionality for the Helpbutton
    def find_possibilties(self, temp_puzzlestring):
        #setup for solver
        self.setup(temp_puzzlestring)
        #fill matrix
        self.value_rule()

        possibilities = {}

        for x in range(self.matrix_size):
            for y in range(self.matrix_size):

                value = int(self.intstring[x * self.matrix_size + y])
                black = True if int(self.colorstring[x * self.matrix_size + y]) == 1 else False
                
                if not value and not black:

                    self.solver.push()
                    self.unique_single_rule(x,y)
                    self.straight_single_rule(x,y)

                    cell = self.value_matrix[x][y]
                    possible_values = []

                    for candidate in range (1, self.matrix_size + 1):
                        self.solver.push()

                        self.solver.assertFormula(self.solver.mkTerm
                                                            (Kind.EQUAL,
                                                            cell,
                                                            self.solver.mkInteger(candidate)))
                        
                        if self.solver.checkSat().isSat():
                            possible_values.append(candidate)

                        self.solver.pop()

                    if possible_values: 
                        possibilities[(x,y)] = possible_values
                        print("List of Possibilities in ",x , y," : ", possible_values)
                       
                    else:
                        print("no help for", x, y)
                    
                    self.solver.pop()

        return possibilities

    def find_value(self, x:int, y:int) -> int:
        value = int(self.intstring[x * self.matrix_size + y])
        return value

    def find_color(self, x: int, y:int) -> bool:
        black = True if int(self.colorstring[x * self.matrix_size + y]) == 1 else False
        return black
    

