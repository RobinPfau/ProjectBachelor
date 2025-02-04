import random
import math
from .smt_v3 import SmtSolver_v3

class SmtCreator():
    def __init__(self, parent):
        # Initialize SmtCreator with the parent app and SMT solver
        self.parent = parent
        self.solver = SmtSolver_v3()
        self.intstring = None
        self.reset_intstring()  # Initialize an empty intstring representing puzzle state
    
    @property
    def difficulty_map(self):
        # Mapping difficulty levels to the number of black cells and initial values
        return {
            "easy": {"n_black": 25, "n_int": 23},
            "medium": {"n_black": 22, "n_int": 19},
            "hard": {"n_black": 22, "n_int": 13},
            "impossible": {"n_black": 21, "n_int": 12}
        }

    def create_seed(self, size, symmetry, difficulty):
        """
        Creates a new puzzleboard with a given size, symmetry, and difficulty.
        """
        n_black = self.difficulty_map[difficulty]["n_black"]
        n_white = 81 - n_black  # Total number of cells minus black cells

        # Adjust black/white cell count for symmetric boards
        if symmetry == "symmetric":
            n_black //= 2
            n_white = 40 - n_black

        # Construct initial cell configuration with shuffled black and white cells
        black = "1" * n_black
        white = "0" * n_white
        stringlist = list(black + white)
        random.shuffle(stringlist)

        colorstring = "".join(stringlist)

        # Handle symmetric board creation by mirroring the pattern
        if symmetry == "symmetric":
            colorstring_two = colorstring[::-1]
            fill = str(random.choice([0, 1]))
            colorstring = colorstring + fill + colorstring_two

        return colorstring

    def fill_seed(self, size):
        """
        Fill initial integer values into the seed based on the difficulty configuration.
        """
        colorlist = list(self.colorstring)
        intlist = list(self.intstring)

        # Randomly insert 5-6 non-zero values in black cells to start puzzle solving
        for _ in range(random.choice([5, 6])):
            non_zero_indices = [i for i, color in enumerate(colorlist) if color == "1" and intlist[i] == "0"]
            index = random.choice(non_zero_indices)
            value = random.choice(range(1, 10))  # Choose a random value between 1-9
            
            temp_intstring = "".join(intlist)
            intlist[index] = str(value)

            # Check if inserting the value breaks basic puzzle constraints
            if self.check_start_value(temp_intstring, size, index // 9, index % 9, value):
                print("found non unique start value at index: ", index)
                intlist[index] = "0"  # Revert if it leads to a conflict

        self.intstring = "".join(intlist)
        return self.intstring + self.colorstring

    def create_puzzle(self, size, symmetry, difficulty):
        """
        Main method to create a new puzzle based on difficulty, size, and symmetry.
        """
        self.colorstring = self.create_seed(size, symmetry, difficulty)
        self.matrix_size = math.sqrt(len(self.colorstring))

        puzzlestring = self.fill_seed(size)
        print(f"creating a {difficulty} {symmetry} puzzle")

        # Attempt to solve the initial puzzle until a valid solution is found
        solutions = self.solver.solve(puzzlestring)
        counter = 0
        while not solutions:
            print(f"failed attempt: #{counter}")
            self.parent.display.update_display("attempt failed")
            self.reset_intstring()
            self.colorstring = self.create_seed(size, symmetry, difficulty)
            puzzlestring = self.fill_seed(size)
            solutions = self.solver.solve(puzzlestring)
            counter += 1

        self.save_solution(solutions)
        puzzlestring = self.intstring + self.colorstring
        solutions = self.solver.solve(puzzlestring)
        print(self.solver.alternate_solution())

        # Attempt to reduce the number of initial clues to meet the desired difficulty
        for attempt in range(5):
            print("this is reduce try number :", attempt + 1)
            n_int = self.difficulty_map[difficulty]["n_int"]
            while len([i for i, value in enumerate(self.intstring) if value != "0"]) > n_int:
                reduced_intstring = self.reduce_solution()
                puzzlestring = reduced_intstring + self.colorstring
                solutions = self.solver.solve(puzzlestring)

                # Check for alternate solutions
                if self.solver.alternate_solution():
                    print("found alternate, restarting loop")
                    break
                self.intstring = reduced_intstring

        print("found non unique")
        print(self.intstring + self.colorstring)
        self.parent.display.update_display(f"created {difficulty} {symmetry}")
        return self.intstring + self.colorstring

    def save_solution(self, solutions):
        """
        Store the solution in the intstring.
        """
        for x, row in enumerate(solutions):
            for y, solution in enumerate(row):
                if solution > 0:
                    index = x * 9 + y
                    stringlist = list(self.intstring)
                    stringlist[index] = str(solution)
                    self.intstring = "".join(stringlist)
        print("saved solution: ", self.intstring)

    def reduce_solution(self):
        """
        Remove random clues while ensuring the puzzle remains solvable with a unique solution.
        """
        stringlist = list(self.intstring)
        non_zero_indices = [i for i, value in enumerate(stringlist) if value != "0" and self.colorstring[i] == "0"]
        index = random.choice(non_zero_indices)
        stringlist[index] = "0"
        return "".join(stringlist)

    def reset_intstring(self):
        """
        Initialize or reset the intstring to represent an empty puzzle.
        """
        self.intstring = "0" * 81

    def check_start_value(self, intstring: str, size: int, x: int, y: int, value: int) -> bool:
        """
        Check if placing a value at a given position violates uniqueness in rows or columns.
        """
        col = [intstring[i * size + y] for i in range(size)]
        row = [intstring[y * size + x] for x in range(size)]
        return str(value) in col or str(value) in row
