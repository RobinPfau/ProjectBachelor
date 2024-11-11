import numpy as np

class Matrix():
    def __init__(self, puzzle):
        self.matrix_size = 9
        self.solved = False
        self.grid = []
        self.grid_t = []
        self.straights = []
        
        self.grid_content = None

        self.puzzle = puzzle
        counter = 0
    
        for row in range(self.matrix_size):
            current_row = []
            for col in range(self.matrix_size):
                self.grid_content = self.puzzle[counter]
                self.grid_content.x = row
                self.grid_content.y = col

                current_row.append(self.grid_content)
                
                counter += 1
                
            self.grid.append(current_row)
        #transposed matrix for checking columns
              

    
    #updates a single cell of the matrix
    def update_matrix(self, x, y, n):
        self.grid[x][y].value = n
        
    
    #loads a new set of values into the matrix, updates straights and transposed matrix
    def reload_matrix(self, newpuzzle):
        counter = 0
        print(counter)
        for row in range(self.matrix_size):
            for col in range(self.matrix_size):
                self.grid_content = newpuzzle[counter]
                self.grid_content.x = row
                self.grid_content.y = col
                self.grid[row][col] = self.grid_content
                counter += 1
            
        self.grid_t = np.array(self.grid).T

        self.straights = self.find_straights()

    #finds all groupings and saves them in a list
    def find_straights(self):

        straights = []
        
        for row in range(self.matrix_size):
            current_straight = []
            listing = False

            for col in range(self.matrix_size):
                color = self.grid[row][col].color

                if color == "black":
                    if listing:
                        if len(current_straight) > 1: 
                            straights.append(current_straight)
                        current_straight = []
                        listing = False                                

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

                if color == "black":
                    if listing:
                        if len(current_straight) > 1: 
                            straights.append(current_straight)
                        current_straight = []
                        listing = False                                

                elif color == "white":
                    if not listing:
                        listing = True
                
                    current_straight.append(self.grid[row][col])

            if len(current_straight) > 1: 
                straights.append(current_straight)

        print(len(straights))
        return straights
    
