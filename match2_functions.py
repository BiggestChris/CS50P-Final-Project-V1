import random
import sys
from os import system, name
from tabulate import tabulate

def main():
    size = set_size()
    try:                                                # This sets the size of the grid - by 4,4 by default or command lines if entered in right format, this also controls incorrect entries
        initial_objects = create_inital_objects(size)   # This creates the actual underlying grid dictionary, and a reveal dictionary which controls the game state
        grid_object = initial_objects[0]                # Maps the output of above to a grid dictionary
        reveal_object = initial_objects[1]              # Maps the output of above to a reveal dictionary
        keys = list(grid_object)                        # Puts the coordinates of our grid into a list for checking against
    except ValueError:
        sys.exit("Error - ValueError on size")
    print_first_table(grid_object, size)                # Prints the initial unrevealed grid to the terminal
    count = 0                                           # Sets a counter to count the number of guesses the user makes
    while True:
        cell_list = select_cells(grid_object, reveal_object, keys, size)    # Asks user to pick cells and prints a grid with them revealed, along with checking if there's a match and returning a list
                                                                            # First item in list is cell1 coordinate, second is cell2 coordinate, third is emoji if they are matching, otherwise it's a hash
        reveal_object[cell_list[0]] = cell_list[2]                          # Sets reveal dictionary value for that coordinate as the underlying emoji revealed
        reveal_object[cell_list[1]] = cell_list[2]                          # Sets reveal dictionary value for that coordinate as the underlying emoji revealed
        count += 1                                                          # Increments number of guesses
        if reveal_object == grid_object:                                    # Breaks the loop to end the game if all cells have been revealed
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


def create_inital_objects(size):
    grid_object = create_grid_object(size)              # Creates the grid dictionary (with emojis populated) based on size
    reveal_object = initialise_reveal(size)             # Creates the reveal dictionary (all hashes by default) based on size
    return grid_object, reveal_object                   # Returns both of these dictionaries as a tuple


def create_grid_object(size):
    pics = initialise(size)                             # Returns the list of emojis based on size
    randomise(pics)                                     # Shuffles the order of the emojis for populating into the grid
    return map_to_grid(pics, size)                      # Maps the emojis to coordinates as a dictionary


def initialise(size):
    emojis_catalogue = [                                # List of emojis to use
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

    if (int(size[0] * size[1]) % 2 != 0) or (int(size[0] * size[1]) > 30):
        raise ValueError

    emojis = []                                         # Empty emoji list to populate
    for num in range(int(size[0] * size[1] / 2)):       # Iterate through size to populate with pairs of emojis
        emojis.append(emojis_catalogue[(2 * num)])
        emojis.append(emojis_catalogue[(2 * num) + 1])

    return emojis


def randomise(list):
    random.shuffle(list)                                # Randomly assort a list (for emojis)

    return list


def map_to_grid(list, size):
    grid = {}                                       # Creates an empty grid dictionary to populate with coordinate-emoji key-value pairs
    rows = []                                       # Creates an empty row list to populate with number of rows (height)
    for num in range(1, (size[1] + 1)):             # Iterates through size number to populate rows list with number of rows, numbered 1+
        rows.append(str(num))
    columns = []                                    # Creates an empty column list to populate with number of columns (width)
    for num in range (97, (size[0] + 97)):          # Iterates through size number to populate column list with lettering of columns, A+, with extra unicode characters beyond z
        columns.append(chr(num))
    i = 0
    j = 0
    for item in list:                               # Moves through the different rows and column permutations to populate with list entries (i.e. assigns emojis to coordinates)
        grid[f"{columns[i]}{rows[j]}"] = item
        if i == (len(columns) - 1):
            if j == (len(rows) - 1):                # Automatically moves when reaching the end of a column or row
                break
            else:
                j += 1
                i = 0
        else:
            i += 1

    return grid                                     # Returns a populated grid dictionary


def initialise_reveal(size):                        # This function is the same as map_to_grid, but populates with hashes instead of emojis
    grid = {}
    rows = []
    for num in range(1, (size[1] + 1)):
        rows.append(str(num))
    columns = []
    for num in range (97, (size[0] + 97)):
        columns.append(chr(num))
    i = 0
    j = 0
    while True:
        grid[f"{columns[i]}{rows[j]}"] = "#"
        if i == (len(columns) - 1):
            if j == (len(rows) - 1):
                break
            else:
                j += 1
                i = 0
        else:
            i += 1

    return grid


def print_first_table(grid_object, size):
    hash_table = grid_to_hash_table(grid_object, size)                              # Takes a grid dictionary and repopulates with hashes and turns to a list so it can be printed with tabular
    print(tabulate(hash_table, tablefmt="grid", colalign=("center","center")))      # Prints the hashed list using tabulate


def grid_to_hash_table(object, size):
    table = [[""]]                                      # Creates an empty table to populate, first column/first row is blank
    for num in range(97, (size[0] + 97)):                   # Populates first row with column letters
        table[0].append(chr(num))
    for num in range(1, (size[1] + 1)):                     # For each row, populates first entry with row number
        try:
            if object[f"a{num}"]:                           # If there's another row then creates that row
                table.append([f"{num}"])
                table = recur_hash(table, object, 97, num)      # Looks to populate with as many columns that exists, then the loop moves to the next row
        except KeyError:
            pass

    return table


def recur_hash(table, object, x, y):
    table_change = table
    try:
        if object[f"{chr(x)}{y}"]:                          # Uses recursion to look to see if another column is there and populating with a hash if so
            table_change[y].append("#")
            return recur_hash(table, object, (x + 1), (y))
    except KeyError:
        return table_change


def select_cells(grid_object, reveal_object, keys, size):
    cell1 = key_input("Cell 1: ", keys, reveal_object)                      # Asks to input a value for the cell, and tests to see if it's valid
    cell2 = key_input("Cell 2: ", keys, reveal_object)                      # Asks to input a value for the cell, and tests to see if it's valid
    if cell2 == cell1:                                                      # Prompts to re-enter cell 2 if it is that same ass cell 1
        while cell2 == cell1:
            print("Cell 2 has to be different from Cell 1")
            cell2 = key_input("Cell 2: ", keys, reveal_object)
    print_reveal_table(grid_object, reveal_object, cell1, cell2, size)      # Prints the table with the two emojis revealed
    return [cell1, cell2, match(grid_object, cell1, cell2)]            # Returns the coordinate of the two cells and tests to see if they match


def key_input(input_text, list, reveal_object):
    while True:
        item = input(input_text).lower()                        # Converts input to lower so case-insensitive
        if item in list:                                        # Checks that the value entered is actually a cell in the grid
            if reveal_object[item] != "#":                      # Checks that the cell hasn't already been revealed
                print("Match already made in that cell")
                continue
            else:
                break
        else:
            print("Please select a cell in the grid")
    return item


def print_reveal_table(grid_object, reveal_object, cell1, cell2, size):
    temp_reveal_table = reveal(grid_object, reveal_object, cell1, cell2, size)              # Creates a temporary list based on the current reveal dictionary and cells revealed
    # For Windows
    system('cls')                                                                           # Clears the terminal - so users can't cheat by looking at previous reveals
    print(tabulate(temp_reveal_table, tablefmt="grid", colalign=("center","center")))       # Uses the above list to print using tabulate


def reveal(object_static, object_dynamic, x, y, size):
    new_table = [[""]]                                                                          # Functions similar to grid_to_hash_table but checking against the grid dictionary
    for num in range(97, (size[0] + 97)):
        new_table[0].append(chr(num))

    for num in range(1, (size[1] + 1)):
        try:                                                                                    # Here this is appending the reveal dictionary values to the tables (not just hashes)
            if object_static[f"a{num}"]:
                new_table.append([f"{num}"])
                new_table = recur_append(new_table, num, object_static, object_dynamic, "a", num, x, y)     # This uses recursion to test if there's a further column
        except KeyError:
            pass

    return new_table


def recur_append(table, position, object_static, object_dynamic, cell_x, cell_y, box1, box2):                       # Recursive function to test if cell is the one revealed should occur then performing
    table_change = table
    table_change[position].append(append_test(object_static, object_dynamic, (str(cell_x) + str(cell_y)), box1, box2))
    try:
        return recur_append(table_change, position, object_static, object_dynamic, chr(ord(cell_x) + 1), cell_y, box1, box2)
    except KeyError:
        return table_change


def append_test(object_static, object_dynamic, cell, box1, box2):
    if object_static[cell]:                                                                 # Checks if the cell being looped through is equal to the one to reveal
        if (cell == box1) or (cell == box2):                                                # If yes then it appends the emoji
            return object_static[cell]
        else:                                                                               # If no then it uses the value already there (hash or revealed emoji)
            return object_dynamic[cell]


def match(grid_object, cell1, cell2):
    if grid_object[cell1] == grid_object[cell2]:        # Function used to determine if the cells revealed a match together
        return grid_object[cell1]                       # If a match it returns the matching emoji
    else:
        return "#"                                      # Otherwise it returns a hash


if __name__ == "__main__":
    main()
