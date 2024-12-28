class Matrix():
    def __init__(self, puzzle, size = 9):
        self.matrix_size = size
        self.solved = False
        self.grid = []
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
        
        self.find_straights()

              
    #updates a single cell of the matrix
    def update_matrix(self, x, y, n):
        self.grid[x][y].value = n
        
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
        self.straights = straights
    
