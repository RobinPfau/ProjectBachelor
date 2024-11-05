

class Matrix():
    def __init__(self, puzzle):
        self.grid = []
        self.grid_content = None
        counter = 0
        for row in range(9):
            current_row = []
            for col in range(9):
                self.grid_content = puzzle[counter]
                current_row.append(self.grid_content)
                counter += 1
                
            self.grid.append(current_row)
        #print(self.grid)

    def update_matrix(x,y,n):
        
        return