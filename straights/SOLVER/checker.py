class Solver ():

    def __init__(self, matrix):
        self.matrix = matrix
    
    def check_duplicates(self):
        duplicates_found = False
    
        # Check for duplicates in rows
        for row_index, row in enumerate(self.matrix.grid):
            seen_values = set()
            for element in row:
                if element.value in seen_values and element.value != 0:
                    print(f"Duplicate value {element.value} found in row {row_index}")
                    duplicates_found = True
                    break
                seen_values.add(element.value)
    
        # Check for duplicates in columns
        for col_index, col in enumerate(self.matrix.grid_t):
            seen_values = set()
            for element in col:
                if element.value in seen_values and element.value != 0:
                    print(f"Duplicate value {element.value} found in column {col_index}")
                    duplicates_found = True
                    break
                seen_values.add(element.value)
    
        # Summary message
        print("no duplicates found")
        return duplicates_found
