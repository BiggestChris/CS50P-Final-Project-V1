import random
import sys
from os import system
from tabulate import tabulate

# A number of functions in here mirror those in match2_functions.py, so less description is given for those

class Grid:                                             # ddbai helped create this
    def __init__(self, size):                                                               # This initialises all the properties of the Grid class
        if not isinstance(size, tuple):                                                     # Raises a Value Error if anything but a tuple is passed
            raise ValueError("Size variable not a tuple")
        else:
            try:                                                                            # Raises a Value Error if tuple doesn't contain integers
                int(size[0])
                int(size[1])
                if (int(size[0]) <= 0) or ((int(size[1]) <= 0)):                            # Raises a Value Error if either integer zero or negative
                    raise ValueError ("Sizes must be positive non-zero integers")
                elif ((int(size[0]) * int(size[1]) % 2) != 0):                              # Raises a Value Error if both integers don't multiply to zero
                    raise ValueError("Size not an even grid")
                elif (int(size[0]) * int(size[1]) > 30):                                    # Raises a Value Error if both integers multiply to more than 30
                    raise ValueError("Maximum number of cells is 30")
                else:
                    self._size = size
            except ValueError:
                raise ValueError("Size must be an integer")
        self._grid, self._reveal = self.__initialise_grid()                                 # Creates grid and reveal properties based on size
        self._table = self.__create_table(self.reveal)                                      # Creates table property based on reveal
        self._keys = list(self.grid)                                                        # Creates keys property based on grid

    def __str__(self):                                                                      # When printing the grid - will produce tabulated table
        return tabulate(self.table, tablefmt="grid", colalign=("center","center"))

    @property                                                                               # Sets properties above so they can't be mutated
    def size(self):
        return self._size

    @property
    def grid(self):
        return self._grid

    @property
    def reveal(self):
        return self._reveal

    @property
    def keys(self):
        return self._keys

    @property
    def table(self):
        return self._table

    def __update_table(self):                                                                   # Internal function to update table property when called
        self._table = self.__create_table(self.reveal)

    def __initialise_grid(self):                                                                # Internal function to create grid and reveal property
        pics = self.__initialise_emojis()
        initial = self.__map_to_grid(pics)
        return initial

    def __initialise_emojis(self):                                                              # Internal function to select emojis based on size and randomise order
        emojis_catalogue = [
            "🌴", "🌴",
            "🍗", "🍗",
            "🚀", "🚀",
            "🐇", "🐇",
            "🐢", "🐢",
            "🐉", "🐉",
            "🍅", "🍅",
            "🍕", "🍕",
            "🍇", "🍇",
            "🌊", "🌊",
            "🍌", "🍌",
            "📙", "📙",
            "🎱", "🎱",
            "🔥", "🔥",
            "💣", "💣"
        ]

        if (int(self.size[0] * self.size[1]) % 2 != 0) or (int(self.size[0] * self.size[1]) > 30):
            raise ValueError

        emojis = []
        for num in range(int(self.size[0] * self.size[1] / 2)):
            emojis.append(emojis_catalogue[(2 * num)])
            emojis.append(emojis_catalogue[(2 * num) + 1])

        random.shuffle(emojis)

        return emojis

    def __map_to_grid(self, list):                                                              # Internal function to create the grid and reveal property as dictionaries based on the size
        pics_grid = {}
        hash_grid = {}
        rows = []
        for num in range(1, (self.size[1] + 1)):
            rows.append(str(num))
        columns = []
        for num in range (97, (self.size[0] + 97)):
            columns.append(chr(num))
        i = 0
        j = 0
        for item in list:
            pics_grid[f"{columns[i]}{rows[j]}"] = item
            hash_grid[f"{columns[i]}{rows[j]}"] = "#"
            if i == (len(columns) - 1):
                if j == (len(rows) - 1):
                    break
                else:
                    j += 1
                    i = 0
            else:
                i += 1

        return pics_grid, hash_grid

    def __create_table(self, dict):                                                             # Internal function to map the reveal property to a table list to run through tabulate
        new_table = [[""]]
        for num in range(97, (self.size[0] + 97)):
            new_table[0].append(chr(num))
        for num in range(1, (self.size[1] + 1)):
            try:
                if dict[f"a{num}"]:
                    new_table.append([f"{num}"])
                    new_table = self.__recur_column(new_table, dict, 97, num)
            except KeyError:
                pass

        return new_table

    def __recur_column(self, table, dict, x, y):                                                # Used to recur in the above function
        new_table = table
        try:
            if dict[f"{chr(x)}{y}"]:
                new_table[y].append(dict[f"{chr(x)}{y}"])
                return self.__recur_column(new_table, dict, (x + 1), (y))
        except KeyError:
            return new_table

    def reveal_cell(self, cell):                                                                # This is a method created to be used to reveal a cell in the Match 2 grid
        try:                                                                                    # If cell variable passed isn't in grid then a Value Error is called
            self._reveal[cell] = self.grid[cell]                                                # Otherwise it will set the reveal reference to the grid reference
        except KeyError:
            raise ValueError("Invalid cell reference")
        self.__update_table()

    def unreveal_cell(self, cell):                                                              # Similar to reveal_cell, this is a method to unreveal a cell in the Match 2 grid and replace it back with a #
        try:
            if cell in self.keys:                                                               # If cell variable passed isn't in the keys then a Value Error will be raised
                self._reveal[cell] = "#"                                                        # Otherwise reveal will have that cell reference changed to #
            else:
                raise ValueError("Invalid cell reference")
        except KeyError:
            raise ValueError("Invalid cell reference")
        self.__update_table()


def main():
    size = set_size()                                                       # Takes a size based on command line inputs
    grid = Grid(size)                                                       # Creates a Grid object passing in the size
    print(grid)                                                             # Prints the grid to the screen
    count = 0                                                               # Sets a counter to count the number of guesses the user makes
    while True:
        cell_list = select_cells(grid)                                      # Asks user to pick cells and prints a grid with them revealed, along with checking if there's a match and returning a list
                                                                            # First item in list is cell1 coordinate, second is cell2 coordinate, third is emoji if they are matching, otherwise it's a hash
        grid.reveal_cell(cell_list[0])
        grid.reveal_cell(cell_list[1])
        # For Windows
        system('cls')
        print(grid)                                                         # Prints the table with the two emojis revealed
        if grid.reveal[cell_list[0]] != grid.reveal[cell_list[1]]:
            grid.unreveal_cell(cell_list[0])
            grid.unreveal_cell(cell_list[1])
        count += 1                                                          # Increments number of guesses
        if grid.reveal == grid.grid:                                        # Breaks the loop to end the game if all cells have been revealed
            break
    sys.exit(f"You win! You used {count} guesses.")                         # Exits the game once the loop has broken

def set_size():
    if len(sys.argv) == 3:                                                  # Runs tests if width and height entered as command line variables
        try:
            int(sys.argv[1])
            int(sys.argv[2])
            if (int(sys.argv[1]) * int(sys.argv[2])) % 2 != 0:              # Exits if width x height isn't even (will not have pairs matching grid)
                sys.exit("Please ensure width x height is an even number")
            else:
                if (int(sys.argv[1]) * int(sys.argv[2])) > 30:              # Exits if width x height is greater than 30 (max emojis)
                    sys.exit("Please ensure width x height is not over 30")
                else:                                                       # Returns size as width, height tuple
                    return (int(sys.argv[1]), int(sys.argv[2]))
        except ValueError:                                                  # Exits if integers are not entered
            sys.exit("Please enter integer for width and height")
    elif len(sys.argv) == 1:                                                # If no command line arguments entered, then defaults to 4 x 4
        return (4, 4)
    else:                                                                   # If wrong number of command line arguments entered, prompts user the correct way
        sys.exit("Usage: match2.py 'width' 'height'")

def select_cells(object):
    cell1 = key_input("Cell 1: ", object)                               # Asks to input a value for the cell, and tests to see if it's valid
    cell2 = key_input("Cell 2: ", object)                               # Asks to input a value for the cell, and tests to see if it's valid
    if cell2 == cell1:                                                  # Prompts to re-enter cell 2 if it is that same ass cell 1
        while cell2 == cell1:
            print("Cell 2 has to be different from Cell 1")
            cell2 = key_input("Cell 2: ", object)
    return [cell1, cell2]                                               # Returns the coordinate of the two cells

def key_input(input_text, object):
    while True:
        item = input(input_text).lower()                        # Converts input to lower so case-insensitive
        if item in object.keys:                                 # Checks that the value entered is actually a cell in the grid
            if object.reveal[item] != "#":                      # Checks that the cell hasn't already been revealed
                print("Match already made in that cell")
                continue
            else:
                break
        else:
            print("Please select a cell in the grid")
    return item


if __name__ == "__main__":
    main()

