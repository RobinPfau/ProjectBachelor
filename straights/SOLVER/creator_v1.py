import cvc5
from cvc5 import Kind

class SmtCreator():
    def __init__(self, size = 9):

        self.solver = cvc5.Solver()
        self.matrix_size = size
        self.solver.setOption("produce-models", "true")

        self.int_sort = self.solver.getIntegerSort()
        self.bool_sort = self.solver.getBooleanSort()

        self.grid_value = [[self.solver.mkConst(self.int_sort, f"value{x}_{y}") for y in range(self.matrix_size)] for x in range(self.matrix_size)] 
        self.grid_color = [[self.solver.mkConst(self.bool_sort, f"color{x}_{y}") for y in range(self.matrix_size)] for x in range(self.matrix_size)] 
    
        self.constraints = []


    def cell_rule(self):
       
       for x in range(self.matrix_size):
           for y in range(self.matrix_size):
                
                #white cells (color = FALSE) must have values between 1 and 9 and are part of straights
                white_cell_constraint = self.solver.mkTerm(
                    Kind.IMPLIES,
                    self.solver.mkTerm(Kind.NOT, self.grid_color[x][y]),                                                #cell is white
                    self.solver.mkTerm(
                        Kind.AND,
                        self.solver.mkTerm(Kind.GEQ, self.grid_value[x][y], self.solver.mkInteger(1)),                        #white cell with a value between 1 and 9
                        self.solver.mkTerm(Kind.LEQ, self.grid_value[x][y], self.solver.mkInteger(self.matrix_size))    
                    )
                )
            
                self.constraints.append(white_cell_constraint)

                #black cells (color = TRUE)  must have values between 1 and 9 or empty (negative)
                black_cell_constraint = self.solver.mkTerm(
                    Kind.IMPLIES, 
                    self.grid_color[x][y],                                                                     #cell is black
                    self.solver.mkTerm(
                        Kind.OR, 
                        self.solver.mkTerm(Kind.LEQ, self.grid_value[x][y], self.solver.mkInteger(-1)),                    #empty black cell
                        self.solver.mkTerm(
                            Kind.AND,
                            self.solver.mkTerm(Kind.GEQ, self.grid_value[x][y], self.solver.mkInteger(1)),                #black cell with a value between 1 and 9
                            self.solver.mkTerm(Kind.LEQ, self.grid_value[x][y], self.solver.mkInteger(self.matrix_size))
                        )
                    )
                )
                self.constraints.append(black_cell_constraint)



    def unique_rule(self):
        #all rows must be filled with distinct values, ignoring empty cells
        for x in range(self.matrix_size):
            row_values = []
            for y in range(self.matrix_size):                 
                row_values.append(self.grid_value[x][y])                                
                print(row_values)           
            row_constraint = self.solver.mkTerm(Kind.DISTINCT, *row_values)                                     #enforce distinct cells
            self.constraints.append(row_constraint)

        #all columns must be filled with distinct values, ignoring empty cells
        for y in range(self.matrix_size):  
            col_values = [self.grid_value[x][y] for x in range(self.matrix_size)]
            print(col_values)              #all cells that arent empty(-1)            
            col_constraint = self.solver.mkTerm(Kind.DISTINCT, *col_values)                                                 #enforce distinct cells
            self.constraints.append(col_constraint)


    def consecutive_rule(self):

        for x in range(self.matrix_size):
            row_values = []

            for y in range(self.matrix_size):
                if self.solver.mkTerm(Kind.NOT, self.grid_color[x][y]):                   # Cell is white
                    row_values.append(self.grid_value[x][y])
                
                else: 
                    if len(row_values) > 1:
                        row_constraint = self.enforce_consecutive(row_values)
                        self.constraints.append(row_constraint)
                    row_values = []

            if len(row_values) > 1:
                row_constraint = self.enforce_consecutive(row_values)
                self.constraints.append(row_constraint)
                row_values = []

 
    def enforce_consecutive(self, values):

        min = self.solver.mkConst(self.int_sort,f"min_{id(values)}" )
        max = self.solver.mkConst(self.int_sort,f"max_{id(values)}" )

        min_constraint = [self.solver.mkTerm(Kind.LEQ, min, value) for value in values]
        max_constraint = [self.solver.mkTerm(Kind.GEQ, max, value) for value in values]
        
        range_constraint = self.solver.mkTerm(
            Kind.EQUAL,
            self.solver.mkTerm(Kind.SUB, max, min), 
            self.solver.mkInteger(len(values) - 1))

        straight_constraint = self.solver.mkTerm(Kind.AND, *(min_constraint + max_constraint + [range_constraint]))
        
        return straight_constraint

        #v1 of restricting blacks
    #def max_black_rule(self):
     #   black_counter = self.solver.mkConst(self.int_sort, "black_counter")
      #  black_count = []
#
 #       for x in range(self.matrix_size):
  #          for y in range(self.matrix_size):
   #             
    #           black_count.append(self.solver.mkTerm(Kind.ITE,
     #                                                   self.grid_color[x][y],   # If the cell is black
      #                                                  self.solver.mkInteger(1), # Then count 1
       #                                                 self.solver.mkInteger(0)))  # Otherwise, count 0
        #
     #   total_black = self.solver.mkTerm(Kind.ADD, *black_count)
      #  self.constraints.append(self.solver.mkTerm(Kind.LEQ, total_black, self.solver.mkInteger(25)))
      # 
     
      #  #v2 of restricting blacks
    def max_black_rule(self):

        for x in range(self.matrix_size):
            black_count= []

            for y in range(self.matrix_size):
                black_count.append(self.solver.mkTerm(Kind.ITE,
                                                        self.grid_color[x][y],   # If the cell is black
                                                        self.solver.mkInteger(1), # Then count 1
                                                        self.solver.mkInteger(0)))  # Otherwise, count 0
            total_black = self.solver.mkTerm(Kind.ADD, *black_count) 
            self.constraints.append(self.solver.mkTerm(Kind.LEQ, total_black, self.solver.mkInteger(3)))     


        for y in range(self.matrix_size):
            black_count= []

            for x in range(self.matrix_size):
                black_count.append(self.solver.mkTerm(Kind.ITE,
                                                        self.grid_color[x][y],   # If the cell is black
                                                        self.solver.mkInteger(1), # Then count 1
                                                        self.solver.mkInteger(0)))  # Otherwise, count 0
            total_black = self.solver.mkTerm(Kind.ADD, *black_count) 
            self.constraints.append(self.solver.mkTerm(Kind.LEQ, total_black, self.solver.mkInteger(3)))



    def solve(self):
        for constraint in self.constraints:
            self.solver.assertFormula(constraint)

        if self.solver.checkSat().isSat():
            print("solution found")
            valuestring = ""
            colorstring = ""
            puzzlestring = ""
        
            for x in range(self.matrix_size):
                
                for y in range(self.matrix_size):
                    # Get the model value for each cell in the grid
                    
                    cell_value = self.solver.getValue(self.grid_value[x][y]).getIntegerValue()
                    if cell_value > 0:
                        valuestring += str(cell_value)
                    else:
                        valuestring += "0"
                #
                    cell_color = self.solver.getValue(self.grid_color[x][y]).getBooleanValue()
                    if cell_color:
                        colorstring += "1"
                    else:
                        colorstring += "0"

            puzzlestring = valuestring + colorstring
            print(puzzlestring)
            return puzzlestring
        else: 
            print("No Puzzle found")
            return None


    def generate_puzzle(self):
        self.cell_rule()
        self.unique_rule()
        self.consecutive_rule()
        self.max_black_rule()
        return self.solve()

