# Match 2 Game
## Video Demo:  <[https://youtu.be/eKFxwbXSmSY](https://youtu.be/eKFxwbXSmSY)>
## Description:

### 1) Summary
For my final project in CS50P I have created a Match 2 game in Python that runs in the terminal.

This game allows the user to select how many rows and columns the grid to play the game will have in the command line (Default is 4 x 4, and maximum number of cells is 30), and then they select pairs of cells to reveal them. When they reveal a pair that match they stay revealed, and once they have revealed all of the pairs the game ends and they are told how many guesses it took them.

#### How to run
match2_objects.py and test_match2_objects.py have been copied over to project.py and test-project.py, but I have kept the original files in for comparison.
Run project.py, match2_functions.py or match2_objects.py with arguments for number of columns then number of rows, for example:
python match2_functions.py 4 3
would create a grid 4 columns wide and 3 rows high.

Ensure that the wcwidth library is installed before playing to ensure that the emojis are displayed correctly in the grid.

### 2) Architecture
This game has actually been built with two scripts that have the same output:
1. match2_functions.py - this uses Functional Programming, and so relies on series of functions being run out of Main to work
2. match2_objects.py - this uses Object-Oriented Programming, and revolves around defining our game state in a Grid class, that then has methods called
on it when the game is played

This was a great exercise in getting to grips with OOP, and I believe that whilst match2_objects.py is better code, I've kept both in for illustrative purposes.

### 3) Functional programming version
#### match2_functions.py:
This file works as follows:
1. Calls the set_size function to read if a size has been inputted in the command line using sys - contains error handling for invalid arguments
2. Creates dictionaries within main via create_initial_objects to manage the game state
a. grid_object is the static dictionary that determines what emoji is in which cell
b. reveal_object is a dynamic dictionary that is initially populated with hashes but is updated as cells are revealed by the user
c. keys is a list of all the cell references in the grid
3. print_first_table then prints the grid to the terminal using the tabulate library (in doing so it turns the reveal_object dictionary into a list)
4. A loop then enters asking the user for cells to reveal and check
5. Error handling is in place on the cell selection by the user
6. If the pair of cells reveals matching emojis then they remain and the reveal_object dict is updated
7. This loop continues until all of the cells are matched and the game ends, feeding back to the user the number of guesses it took

#### test_match2_functions.py:
This file is the testing file for the above using pytest. Note that random.seed is used to fix random variables in the grid, patch('builtins.print') is used to test that the print output is as expected, and monkeypatch is used to mimic user inputs when asked.

### 4) Object-oriented programming version
#### match2_objects.py:
This file works as follows:
1. Defines the Grid class, with a size tuple being entered upon initialisation (number of columns, number of rows)
2. Initialises with properties for:
size - based on the size tuple, there is error handling in place for passing an invalid size to the Grid class
grid - the fixed mapping of emojis to cells as a dict
reveal - the dynamic mapping of what's been revealed to cells as a dict
table - the mapping of the reveal dict to a list for use in tabulate
keys - the list of cell references in the grid
3. The str functioned is defined so that print(Grid) will show the table itself that the user should see
4. Internal functions are used in defining the above, these should only be used internally and not called as methods on the Class itself
5. Two methods are defined for the class reveal_cell(cell) and unreveal_cell(cell) which should be used to reveal a cell on the grid, or to revert it back to hash respectively (error handling is in place for a cell not in the grid)
6. The main function will run a set_size function to read the user input in the command line for grid size
7. A loop will then be entered as the game is played, with user prompted to select cells and see if they match (with error handling for incorrect cells)
8. This will use reveal_cell to show the user cells, and then unreveal_cell to revert back unless they match in which case unreveal_cell isn't run
9. Once all pairs are revealed the game ends and user is told their number of guesses

#### test_match2_objects.py:
This file is the testing file for the above using pytest. Note that random.seed is used to fix random variables in the grid, patch('builtins.print') is used to test that the print output is as expected, and monkeypatch is used to mimic user inputs when asked. For testing print(grid) - print(str(grid)) was used to check that the grid string is being pulled.
