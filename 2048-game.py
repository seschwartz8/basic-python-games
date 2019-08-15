"""
2048 game by Sarah Schwartz.
"""

import poc_2048_gui #basic graphics provided by Coursera
import random

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def game_state(state):
    """
    Function that adjusts for game state
    """
    if state == "on":
        print "game started"
    elif state == "off":
        print "game over"




def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # create result that's a copy of the line
    merged_line = list(line)
    # slide all non-0's to beginning of result
    if 0 in merged_line:
        for var_i in list(merged_line):
            if var_i == 0:
                merged_line.remove(var_i)
                merged_line.append(var_i)
    # check for duplicates in list
    for var_j in range(len(list(merged_line)) - 1):
        if merged_line[var_j] == merged_line[var_j+1] != 0:
            merged_line.pop(var_j+1)
            merged_line[var_j] = merged_line[var_j]*2
            merged_line.append(0)
    return merged_line



class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid_values = []
        self.reset()
        #initial tile values of up and down direction
        self._up_initials = []
        self._down_initials = []
        for col in range(grid_width):
            self._up_initials.append((0, col))
            self._down_initials.append(((grid_height - 1), col))
        #initial tile values for left and right direction
        self._left_initials = []
        self._right_initials = []
        for row in range(grid_height):
            self._left_initials.append((row, 0))    
            self._right_initials.append((row, (grid_width - 1)))
        #create dictionary of direction initial tiles
        self._direction_initials = {UP : self._up_initials, DOWN : self._down_initials,
                                  LEFT : self._left_initials, RIGHT : self._right_initials}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """ 
        self._grid_values = [[0 for dummy_col in range(self._grid_width)]
                               for dummy_row in range(self._grid_height)]
        for dummy_i in range(2):
            self.new_tile()
        

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        print "Grid values:"
        for row in range(self._grid_height):
            print self._grid_values[row]
        return ""

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction == UP or direction == DOWN:
            num_iter = self._grid_height
        elif direction == RIGHT or direction == LEFT:
            num_iter = self._grid_width
  
        for initial in self._direction_initials[direction]:
            line = []
            count = 0
            #get the value of the tiles plus the offset
            for var_i in range(num_iter):
                line.append(self.get_tile((initial[0] + OFFSETS[direction][0]*var_i), 
                                          (initial[1] + OFFSETS[direction][1]*var_i)))
            #merge the line and replace it
            for merged_val in list(merge(line)):
                self.set_tile((initial[0] + OFFSETS[direction][0]*count), 
                              (initial[1] + OFFSETS[direction][1]*count), 
                              merged_val)
                count += 1
        #spawn new tile
        self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #set tile value to 2 90% of the time and 4 10%
        if random.randrange(0,10) < 9:
            new_value = 2
        else:
            new_value = 4
        #get coordinates of all current empty squares
        empty_squares = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self.get_tile(row, col) == 0:
                    empty_squares.append((row, col))
        #add new tile to random empty square
        if len(empty_squares) > 0: 
            new_loc = random.choice(empty_squares)
            self.set_tile(new_loc[0], new_loc[1], new_value)        
                
                
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid_values[row][col] = value


    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid_values[row][col]

    


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
