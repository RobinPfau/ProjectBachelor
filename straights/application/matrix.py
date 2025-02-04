import math

class Matrix():
    def __init__(self, puzzle):
        self.matrix_size = int(math.sqrt(len(puzzle)))  # size of the matrix
        self.solved = False                             # state of the matrix
        self.grid = []                                  # matrix grid elements             
        self.straights = []                             # list of straights for GUI                    
        
        self.grid_content = None

        self.puzzle = puzzle
        counter = 0
        # create the matrix
        for row in range(self.matrix_size):
            current_row = []
            for col in range(self.matrix_size):
                # create a cell
                self.grid_content = self.puzzle[counter]     # value of the cell
                self.grid_content.x = row                    # row of the cell
                self.grid_content.y = col                    # column of the cell        
                # add the cell to the row
                current_row.append(self.grid_content)
                
                counter += 1
                
            self.grid.append(current_row)
        
        self.find_straights()
            
    #updates a single cell of the matrix
    def update_matrix(self, x, y, n):
        self.grid[x][y].value = n
        
    #finds all groupings and saves them in a list : GUI
    def find_straights(self):
        straights = []     
        for row in range(self.matrix_size):
            current_straight = []
            listing = False

            for col in range(self.matrix_size):
                color = self.grid[row][col].color
                # black color cells are not part of the straight
                if color == "black":
                    if listing:
                        # if the straight has more than one cell, add it to the list
                        if len(current_straight) > 1: 
                            straights.append(current_straight)

                        current_straight = []
                        listing = False                                
                # white color cells are part of the straight
                elif color == "white":
                    if not listing:
                        listing = True
                    
                    current_straight.append(self.grid[row][col])

            if len(current_straight) > 1:  
                straights.append(current_straight)
        
        for col in range(self.matrix_size):
            current_straight = []
            listing = False

            for row in range(self.matrix_size):
                color = self.grid[row][col].color
                # black color cells are not part of the straight
                if color == "black":
                    if listing:
                        # if the straight has more than one cell, add it to the list
                        if len(current_straight) > 1: 
                            straights.append(current_straight)
                            
                        current_straight = []
                        listing = False                                
                # white color cells are part of the straight
                elif color == "white":
                    if not listing:
                        listing = True
                
                    current_straight.append(self.grid[row][col])

            if len(current_straight) > 1: 
                straights.append(current_straight)
        self.straights = straights
    
