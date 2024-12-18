class PuzzleController:
    def __init__(self, matrix, grid):
        self.matrix = matrix
        self.grid = grid
        self.controller = self

    def update_cell_value(self, x, y, value):
        """Updates the value in both the matrix and grid."""
        if self.matrix.is_valid_placement(x, y, value):
            self.matrix.update_matrix(x, y, value)
            self.grid.update_cell_display(x, y, value)
        else:
            self.grid.update_cell_display(x, y, "", color="red")

    def highlight_group(self, x, y):
        """Highlights the group (row, column, or other) for a cell."""
        group = self.matrix.get_group(x, y)  # A method in Matrix to fetch the group
        self.grid.highlight_cells([(c.x, c.y) for c in group])

    def clear_highlight(self):
        """Clears all highlights in the grid."""
        self.grid.clear_highlights()

    def check_solution(self):
        """Compares the grid's state with the solution."""
        return self.matrix.check_solution()