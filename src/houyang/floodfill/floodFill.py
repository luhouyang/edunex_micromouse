###########
# imports #
###########

import API
import sys

from MOUSE import SimulationMouse, RealMouse

#######################
# initialize variable #
#######################

# the mouse's current (x, y) position in the maze
x = 0
y = 0

# the mouse's previous (x, y) position in the maze
xprev = 0
yprev = 0

# state of the mouse, tracks the path finding progress
state = 0

# flag to switch to shortest path mode
short = False

# the mouse's orientation
'''
orients :
    0- North
    1- East
    2- South
    3- West 
'''
orientation = 0

# direction of movement for mouse, can be 'F', 'L', 'R' or 'B'
move_direction = 'F'

# the mouses current cell in the maze
cell = 0

# maze, cell, flood array indexing follows Cartesian coordinates
#
# example:
# cells = [
#           [c, d],
#           [a, b]
#         ]
#
# in the above example "a" is at (0, 0), "b" at (1, 0), "c" at (0, 1), "d" at (1, 1)
# where coordinates are represented as (x, y)
cells = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

flood = [[14, 13, 12, 11, 10, 9, 8, 7, 7, 8, 9, 10, 11, 12, 13, 14],
         [13, 12, 11, 10, 9, 8, 7, 6, 6, 7, 8, 9, 10, 11, 12, 13],
         [12, 11, 10, 9, 8, 7, 6, 5, 5, 6, 7, 8, 9, 10, 11, 12],
         [11, 10, 9, 8, 7, 6, 5, 4, 4, 5, 6, 7, 8, 9, 10, 11],
         [10, 9, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 9, 10],
         [9, 8, 7, 6, 5, 4, 3, 2, 2, 3, 4, 5, 6, 7, 8, 9],
         [8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
         [7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7],
         [7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7],
         [8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
         [9, 8, 7, 6, 5, 4, 3, 2, 2, 3, 4, 5, 6, 7, 8, 9],
         [10, 9, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 9, 10],
         [11, 10, 9, 8, 7, 6, 5, 4, 4, 5, 6, 7, 8, 9, 10, 11],
         [12, 11, 10, 9, 8, 7, 6, 5, 5, 6, 7, 8, 9, 10, 11, 12],
         [13, 12, 11, 10, 9, 8, 7, 6, 6, 7, 8, 9, 10, 11, 12, 13],
         [14, 13, 12, 11, 10, 9, 8, 7, 7, 8, 9, 10, 11, 12, 13, 14]]

flood2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

queue = []

shortest_path = []

#########
# utils #
#########


# print a message to the mms console
def log(msg):
    sys.stderr.write(f"{msg}\n")


# reset states
def reset():
    API.ackReset()
    API.clearAllColor()
    API.clearAllText()

    res = API.wasReset()

    return res


# show info on simulator
def show(flood, variable):
    for x in range(16):
        for y in range(16):
            # TODO implement code for other algorithms
            API.setText(x, y, str(flood[y][x]))


#########################
# check state functions #
#########################

# check if mouse can move to a cell

# check for center

# get (x, y) of surrounding cells

##########################
# update state functions #
##########################


# update walls
def updateWalls(x, y, orientation, color='G'):
    API.setColor(x, y, color)

    L = API.wallLeft()
    R = API.wallRight()
    F = API.wallFront()


# update orientation

# update coordinates

# append zero to center cells

# change destination of mouse

# append destination

##################
# move functions #
##################


# next move functions
def nextMove(x, y, orientation):
    pass


# move
def move():
    pass


# shortest path

# inverse path

# floodfill algorithm

# path inverser

# shortest path

########
# main #
########


def main():

    while (True):
        updateWalls(x, y, orientation)

        # check if at goal
        if ():
            pass

            # get inverse path from center to start

            # follow shortest path

        else:
            pass

            # assign value in current cell

            # look for next reachable cell with lowest value

            # update flood fill array

            # change orientation

            # move forward


if __name__ == '__main__':
    main()
