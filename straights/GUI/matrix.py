

class Matrix():
    def __init__(self, puzzle):
        self.solved = False
        self.grid = []
        self.grid_content = None
        
        self.puzzle = puzzle
        counter = 0
        for row in range(9):
            current_row = []
            for col in range(9):
                self.grid_content = self.puzzle[counter]
                current_row.append(self.grid_content)
                counter += 1
                
            self.grid.append(current_row)

    #updates a single cell of the matrix
    def update_matrix(self, x, y, n):
        self.grid[x][y].value = n
        print(self.grid[x][y].value)
    
    #loads a new set of values into the matrix
    def reload_matrix(self, newpuzzle):
         counter = 0
         for row in range(9):
            for col in range(9):
                self.grid_content = newpuzzle[counter]
                self.grid[row][col] = self.grid_content
                counter += 1