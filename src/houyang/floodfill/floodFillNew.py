#%%

###########
# imports #
###########

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
# replace 'houyang' with your name space
sys.path.insert(
    1, 'C:/Users/User/Desktop/Python/micromouse/edunex_micromouse/src/houyang')

import API
import sys
import numpy as np

from MOUSE import SimulationMouse, RealMouse

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


from colorama import Fore


# show local memory maze state
def showMaze(mx, my, orientation, history, wall_position, flood):
    wall_width = len(wall_position[0])
    wall_height = len(wall_position)

    maze_width = len(flood[0])
    maze_height = len(flood)

    mx = mx * 2 + 1
    my = wall_height - (my * 2 + 1) - 1

    h = []
    for cell in history:
        h.append([cell[0] * 2 + 1, wall_height - (cell[1] * 2 + 1) - 1])

    for (y) in range(wall_height):
        for (x) in range(wall_width):
            if (wall_position[y][x] == 1):
                print(Fore.RED + 'X', end=' ')
            elif (mx == x and my == y):
                if (orientation == 0):
                    print(Fore.CYAN + 'N', end=' ')
                elif (orientation == 1):
                    print(Fore.CYAN + 'E', end=' ')
                elif (orientation == 2):
                    print(Fore.CYAN + 'S', end=' ')
                else:
                    print(Fore.CYAN + 'W', end=' ')
            else:
                if (x % 2 == 1 and y % 2 == 1):
                    if [x, y] in h:
                        val = str(flood[maze_height - int((y - 1) / 2) -
                                        1][int((x - 1) / 2)])
                        if (len(val) == 1):
                            print(Fore.GREEN + val, end=' ')
                        else:
                            print(Fore.GREEN + val, end='')
                    else:
                        val = str(flood[maze_height - int((y - 1) / 2) -
                                        1][int((x - 1) / 2)])
                        if (len(val) == 1):
                            print(Fore.WHITE + val, end=' ')
                        else:
                            print(Fore.WHITE + val, end='')
                else:
                    if (x == 0 or x == wall_width - 1 or y == 0
                            or y == wall_height - 1):
                        print(Fore.BLUE + '.', end=' ')
                    elif (x % 2 == 0 and y % 2 == 0):
                        print(Fore.WHITE + ' ', end=' ')
                    elif (x % 2 == 0 and y % 2 == 1):
                        print(Fore.WHITE + '_', end=' ')
                    else:
                        print(Fore.WHITE + '|', end=' ')
        print(Fore.WHITE + '')


# unpack map txt file to map array
def createMazeFromFile():
    pass

    # read file contents

    # initialize padded array

    # parse file & insert walls


#########################
# check state functions #
#########################


# check for goal
def checkGoal(x, y, flood):
    cell_val = flood[y][x]

    if (cell_val == 0):
        return True
    else:
        False


# get (x, y) of surrounding cells
def getSurround(x, y, flood):
    surrounding_cells = []

    surrounding_cells.append([x, y + 1])  # north
    surrounding_cells.append([x + 1, y])  # east
    surrounding_cells.append([x, y - 1])  # south
    surrounding_cells.append([x - 1, y])  # west

    removed_cells = [
        cell for cell in surrounding_cells
        if (cell[0] < 0 or cell[0] > len(flood[0]) -
            1 or cell[1] < 0 or cell[1] > len(flood) - 1)
    ]

    remaining_cell_index = {
        i: cell
        for i, cell in enumerate(surrounding_cells)
        if cell not in removed_cells
    }

    surrounding_cells = [
        cell for cell in surrounding_cells if cell not in removed_cells
    ]

    # for cell in surrounding_cells:
    #     if (cell[0] < 0 or cell[0] > maze_width-1 or cell[1] < 0 or cell[1] > maze_height-1):
    #         removed_cells.append(cell)

    # for cell in removed_cells:
    #     surrounding_cells.remove(cell)

    return surrounding_cells, remaining_cell_index


# check if mouse can move to a cell
def isAccessible(x, y, wall_position, flood):
    # get surrounding cells
    surrounding_cells, _ = getSurround(x, y, flood)

    # check with wall_position
    '''
    since walls will be at even index 0, 2, 4, ..., 32
    and mouse will be at odd index 1, 3, 5, ..., 31
    mouse position = (x * 2 + 1, y * 2 + 1)
    '''
    x = x * 2 + 1
    y = y * 2 + 1

    wall_arr = np.array(wall_position)
    wall_width = wall_arr.shape[1] - 1
    wall_height = wall_arr.shape[0] - 1

    removed_cells = []

    for cell in surrounding_cells:
        temp = [cell[0] * 2 + 1, cell[1] * 2 + 1]
        '''
        find difference between surrounding cell and position for the axis that is different
        the difference will be equal to the wall index in between the cells
        example: for (3, 1) & (1, 1) minus the 'x' axis = (2, 1)
        because 'y' is the same for both
        '''

        if (temp[0] == x):
            wall_cell = [temp[0], int((temp[1] + y) / 2)]
        else:
            wall_cell = [int((temp[0] + x) / 2), temp[1]]
        '''
        reverse indexing for height, y, first dimension of the array
        '''
        # TESTING CODE
        # print(f"CHECK WALL AT: ({wall_cell[0]}, {wall_height - wall_cell[1]}) VALUE: {wall_position[wall_height - wall_cell[1]][wall_cell[0]]}")
        if (wall_position[wall_height - wall_cell[1]][wall_cell[0]] == 1):
            removed_cells.append(cell)

    surrounding_cells = [
        cell for cell in surrounding_cells if cell not in removed_cells
    ]

    # return accessible cells x, y, value
    return surrounding_cells


##########################
# update state functions #
##########################


# update walls
def updateWallsFloodFill(x, y, orientation, color='G'):
    API.setColor(x, y, color)

    L = API.wallLeft()
    R = API.wallRight()
    F = API.wallFront()

    # update wall_position with walls


# update orientation
def updateOrientation(orientation, turn):
    # update orientation based on turn direction
    if (turn == 'L'):
        orientation -= 1
        if (orientation == -1):
            orientation = 3
    elif (turn == 'R'):
        orientation += 1
        if (orientation == 4):
            orientation = 0
    elif (turn == 'B'):
        if (orientation == 0):
            orientation = 2
        elif (orientation == 1):
            orientation = 3
        elif (orientation == 2):
            orientation = 0
        elif (orientation == 3):
            orientation = 1

    return (orientation)


# update coordinates

# append zero to center cells

# change destination of mouse

# append destination

##################
# move functions #
##################


# next move functions
def nextMove(x, y, orientation, wall_position, flood):
    cell_val = flood[y][x]

    # get surrounding cells
    surrounding_cells, remaining_cell_index = getSurround(x, y, flood)

    # get accessible cells
    accessible_cells = isAccessible(x, y, wall_position, flood)

    # compare adjacent cell values with current cell_val
    for cell in accessible_cells:
        adj_val = flood[cell[1]][cell[0]]

        if (cell_val - 1 == adj_val):
            next_cell = cell
            break

    # get turn orientation
    '''
    orients :
        0- North
        1- East
        2- South
        3- West 
    '''
    turning = 'F'
    next_key = [
        key for key, val in remaining_cell_index.items() if val == next_cell
    ][0]

    if (orientation == next_key):
        print("NO NEED TO TURN")
        turning = 'F'
    elif ((orientation + 1) % 4 == next_key):
        # API.turnRight()
        print("TURN RIGHT")
        turning = 'R'
    elif ((orientation - 1) % 4 == next_key):
        # API.turnLeft()
        print("TURN LEFT")
        turning = 'L'
    else:
        # API.turnLeft()
        # API.turnLeft()
        print("TURN BACK")
        turning = 'B'

    orientation == next_key

    # call updateOrientation
    orientation = updateOrientation(orientation, turning)

    # call move
    move(next_cell)

    return orientation, next_cell[0], next_cell[1]


# move
def move(next_cell):
    # call API to move
    # API.moveForward()
    print(f"MOVE TO: {next_cell}")

    # update mouse state

    # call path finding algorithm


# shortest path


# inverse path
def inversePath(path):
    pass


# floodfill algorithm
def floodFill(flood, wall_position):
    width = len(flood[0])
    height = len(flood)

    queue = []

    flood_zero = [[-1] * width for _ in range(height)]

    for y in range(int(height / 2) - 1, int(height / 2) + 1):
        for x in range(int(width / 2) - 1, int(width / 2) + 1):
            queue.append([x, y])
            flood_zero[y][x] = 0

    while (len(queue) != 0):
        x, y = queue.pop(0)

        next_cell_val = flood_zero[y][x] + 1

        accessible_cells = isAccessible(x, y, wall_position, flood)

        for ax, ay in accessible_cells:
            if (flood_zero[ay][ax] == -1):
                flood_zero[ay][ax] = next_cell_val

                queue.append([ax, ay])

    for i in range(16):
        flood[height - i - 1] = flood_zero[height - i - 1]

    return flood


########
# main #
########


def main():
    #######################
    # initialize variable #
    #######################

    # maze, cell, flood array indexing follows Cartesian coordinates
    '''
    example:
    cells = [
            [c, d],
            [a, b]
            ]

    in the above example "a" is at (0, 0), "b" at (1, 0), "c" at (0, 1), "d" at (1, 1)
    where coordinates are represented as (x, y)

    16x16 for all possible mouse positions

    cell_position = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    '''
    ###
    '''
    17x17 + 16x16 since walls are in beteen cells
    33x33 since walls are in beteen cells
    1 - wall is present
    0 - no wall

    sample starting maze
    1 1 1 1
    1 0 0 1
    1 0 0 1
    1 1 1 1
    '''
    wall_position = [[
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ],
                     [
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                     ]]

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

    # the mouse's current (x, y) position in the maze
    X = 0
    Y = 0

    # current cell value
    cell_val = 0

    # the mouse's previous (x, y) position in the maze
    xprev = 0
    yprev = 0

    # state of the mouse, tracks the path finding progress
    # 0, 1, 2, 3 for each corner
    # 5, 6, 7 for going to goal, going to start, switch to short path
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

    ###################
    # Micromouse Code #
    ###################

    shortest_path = []

    history = []

    while (True):
        # updateWallsFloodFill(X, Y, orientation)

        # check if at goal
        if (checkGoal(X, Y, flood)):
            print("DONE!")
            break

            # inverse path from center to start

            # follow shortest path

        else:
            history.append([X, Y])
            showMaze(X, Y, orientation, history, wall_position, flood)
            orientation, X, Y = nextMove(X, Y, orientation, wall_position,
                                         flood)
            flood = floodFill(flood, wall_position)
            print()

            # assign value in current cell

            # look for next reachable cell with lowest value

            # update flood fill array

            # change orientation

            # move forward


if __name__ == '__main__':
    main()

#%%
