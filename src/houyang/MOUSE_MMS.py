#    General Logic & Utility Functions of a Micromouse in classes
#
#        1) SimulationMouse
#              - used for mms simulation
#
#    Example code in README.md
# ========================================================================

###########
# imports #
###########

import API
import sys
import numpy as np

##########################
# simulation mouse class #
##########################


class SimulationMouse():

    def __init__(self):
        pass

    #########
    # utils #
    #########

    # print a message to the mms console
    def log(self, msg):
        sys.stderr.write(f"{msg}\n")

    # reset states
    def reset(self):
        API.ackReset()
        API.clearAllColor()
        API.clearAllText()

        res = API.wasReset()

        return res

    # show info on simulator
    def show(self, flood):
        for x in range(16):
            for y in range(16):
                # TODO implement code for other algorithms
                API.setText(x, y, str(flood[y][x]))

    # show local memory maze state
    def show_maze_QT(self, mx, my, orientation, history, wall_position, flood):
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
            line = ''
            for (x) in range(wall_width):
                if (wall_position[y][x] == 1):
                    line += '##'
                elif (mx == x and my == y):
                    if (orientation == 0):
                        line += 'N '
                    elif (orientation == 1):
                        line += 'E '
                    elif (orientation == 2):
                        line += 'S '
                    else:
                        line += 'W '
                else:
                    if (x % 2 == 1 and y % 2 == 1):
                        if [x, y] in h:
                            val = str(flood[maze_height - int((y - 1) / 2) -
                                            1][int((x - 1) / 2)])
                            if (len(val) == 1):
                                line += val + '-'
                            else:
                                line += val
                        else:
                            val = str(flood[maze_height - int((y - 1) / 2) -
                                            1][int((x - 1) / 2)])
                            if (len(val) == 1):
                                line += val + '-'
                            else:
                                line += val
                    else:
                        if (x == 0 or x == wall_width - 1 or y == 0
                                or y == wall_height - 1):
                            line += '##'
                        elif (x % 2 == 0 and y % 2 == 0):
                            line += '  '
                        elif (x % 2 == 0 and y % 2 == 1):
                            line += '--'
                        else:
                            line += '| '
            self.log(line)
            self.log('\n')

    ##############
    # algorithms #
    ##############

    # floodfill algorithm
    """
    PSEUDOCODE

    1. INITIALIZE 
        queue = empty list
        initial_flood = 2D list fill with -1
    2. ENQUEUE all cell with value = 0
    3. WHILE queue IS NOT EMPTY
    4.      current_cell = queue.pop()
    5.      next_value = current_cell_value + 1
    6.      GET accessible cells from current_cell
    7.      if accessible cells == -1
    8.          ASSIGN cell value = next_value
    9.          ENQUEUE accessible cell
    """

    def floodfill_algorithm(self, flood, wall_position):
        width = len(flood[0])
        height = len(flood)

        queue = []

        flood_zero = [[-1] * width for _ in range(height)]

        for y in range(height):
            for x in range(width):
                if (flood[y][x] == 0):
                    queue.append([x, y])
                    flood_zero[y][x] = 0

        while (len(queue) != 0):
            x, y = queue.pop(0)

            next_cell_val = flood_zero[y][x] + 1

            accessible_cells = self.is_accessible(x, y, wall_position, flood)

            for ax, ay in accessible_cells:
                if (flood_zero[ay][ax] == -1):
                    flood_zero[ay][ax] = next_cell_val

                    queue.append([ax, ay])

        for i in range(16):
            flood[height - i - 1] = flood_zero[height - i - 1]

        return flood

    def predict_path_floodfill(self, X, Y, wall_position, flood, shortest_path,
                               history):
        x = X
        y = Y

        cell_val = flood[y][x]

        recolor_cells_green = [
            cell for cell in shortest_path if cell in history
        ]
        recolor_cells_colorless = [
            cell for cell in shortest_path if cell not in recolor_cells_green
        ]

        for cell in recolor_cells_green:
            API.setColor(cell[0], cell[1], 'G')

        for cell in recolor_cells_colorless:
            API.clearColor(cell[0], cell[1])

        shortest_path = []

        while (cell_val != 0):
            # get accessible cells
            accessible_cells = self.is_accessible(x, y, wall_position, flood)

            # compare adjacent cell values with current cell_val
            for cell in accessible_cells:
                adj_val = flood[cell[1]][cell[0]]

                if (cell_val - 1 == adj_val):
                    shortest_path.append(cell)
                    x = cell[0]
                    y = cell[1]
                    cell_val -= 1
                    break

        for cell in shortest_path:
            API.setColor(cell[0], cell[1], 'a')

        return shortest_path

    # dfs algorithm
    def backtrace_dfs(self, x, y, orientation, wall_position, lifo_stack,
                      trace_stack, maze_state, history):

        x, y = trace_stack.pop(0)

        while (True):
            # get surrounding cells
            surrounding_cells, remaining_cell_index = self.get_surround(
                x, y, maze_state)

            accessible_cells = self.is_accessible(x, y, wall_position,
                                                  maze_state)

            visited_cell = [
                cell for cell in accessible_cells
                if maze_state[cell[1]][cell[0]] == 1
            ]

            accessible_cells = [
                cell for cell in accessible_cells if cell not in visited_cell
            ]

            if (len(accessible_cells) == 0):

                next_cell = trace_stack.pop(0)

                turning = 'F'
                next_key = [
                    key for key, val in remaining_cell_index.items()
                    if val == next_cell
                ][0]

                if (orientation == next_key):
                    turning = 'F'
                elif ((orientation + 1) % 4 == next_key):
                    API.turnRight()
                    turning = 'R'
                elif ((orientation - 1) % 4 == next_key):
                    API.turnLeft()
                    turning = 'L'
                else:
                    API.turnLeft()
                    API.turnLeft()
                    turning = 'B'

                orientation == next_key

                # call updateOrientation
                orientation = self.update_orientation(orientation, turning)

                # call move
                self.move(next_cell)
            else:
                trace_stack.insert(0, [x, y])
                break

            x, y = next_cell

        return orientation, x, y

    def next_move_dfs(self, x, y, orientation, wall_position, lifo_stack,
                      trace_stack, maze_state, history, cell_parent_map):
        # mark cell as visited
        maze_state[y][x] = 1

        # get surrounding cells
        surrounding_cells, remaining_cell_index = self.get_surround(
            x, y, maze_state)

        # get accessible cells
        accessible_cells = self.is_accessible(x, y, wall_position, maze_state)

        visited_cell = [
            cell for cell in accessible_cells
            if maze_state[cell[1]][cell[0]] == 1
        ]

        accessible_cells = [
            cell for cell in accessible_cells if cell not in visited_cell
        ]

        if (len(accessible_cells) != 0):
            for cell in accessible_cells:
                lifo_stack.insert(0, cell)
                cell_parent_map[(cell[0], cell[1])] = [x, y]

            while (True):
                cell = lifo_stack.pop(0)
                if (maze_state[cell[1]][cell[0]] == -1):
                    next_cell = cell
                    trace_stack.insert(0, cell)
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
                key for key, val in remaining_cell_index.items()
                if val == next_cell
            ][0]

            if (orientation == next_key):
                turning = 'F'
            elif ((orientation + 1) % 4 == next_key):
                API.turnRight()
                turning = 'R'
            elif ((orientation - 1) % 4 == next_key):
                API.turnLeft()
                turning = 'L'
            else:
                API.turnLeft()
                API.turnLeft()
                turning = 'B'

            orientation == next_key

            # call updateOrientation
            orientation = self.update_orientation(orientation, turning)

            # call move
            self.move(next_cell)

            return orientation, next_cell[0], next_cell[1]
        else:
            orientation, x, y = self.backtrace_dfs(x, y, orientation,
                                                   wall_position, lifo_stack,
                                                   trace_stack, maze_state,
                                                   history)

            return self.next_move_dfs(x, y, orientation, wall_position,
                                      lifo_stack, trace_stack, maze_state,
                                      history, cell_parent_map)

    # bfs algorithm
    def backtrace_bfs(self, x, y, orientation, wall_position, maze_state,
                      fifo_queue, cell_parent_map, next_cell):

        current_cell = [x, y]
        goal_cell = next_cell
        back_trace = []
        forward_trace = []
        full_trace = []

        # trace from goal
        while (True):
            if ((next_cell[0], next_cell[1]) == (0, 0)):
                break

            next_cell = cell_parent_map[(next_cell[0], next_cell[1])]

            # get accessible cells
            accessible_cells = self.is_accessible(0, 0, wall_position,
                                                  maze_state)

            if (next_cell in accessible_cells):
                back_trace.insert(0, next_cell)
                back_trace.append(goal_cell)
                break
            else:
                back_trace.insert(0, next_cell)

        # trace from current
        next_cell = current_cell
        while (True):
            if ((next_cell[0], next_cell[1]) == (0, 0)):
                break

            next_cell = cell_parent_map[(next_cell[0], next_cell[1])]

            # get accessible cells
            accessible_cells = self.is_accessible(0, 0, wall_position,
                                                  maze_state)

            if (next_cell in accessible_cells):
                forward_trace.insert(0, next_cell)
                break
            else:
                forward_trace.insert(0, next_cell)

        common_nodes = [node for node in forward_trace if node in back_trace]

        closest_ancestor = common_nodes[len(common_nodes) - 1]

        for i in range(forward_trace.index(closest_ancestor),
                       len(forward_trace)):
            full_trace.insert(0, forward_trace[i])

        for i in range(
                back_trace.index(closest_ancestor) + 1, len(back_trace)):
            full_trace.append(back_trace[i])

        while (len(full_trace) > 0):
            next_cell = full_trace.pop(0)

            x, y = current_cell

            # get surrounding cells
            surrounding_cells, remaining_cell_index = self.get_surround(
                x, y, maze_state)

            turning = 'F'
            next_key = [
                key for key, val in remaining_cell_index.items()
                if val == next_cell
            ][0]

            if (orientation == next_key):
                turning = 'F'
            elif ((orientation + 1) % 4 == next_key):
                API.turnRight()
                turning = 'R'
            elif ((orientation - 1) % 4 == next_key):
                API.turnLeft()
                turning = 'L'
            else:
                API.turnLeft()
                API.turnLeft()
                turning = 'B'

            orientation == next_key

            # call updateOrientation
            orientation = self.update_orientation(orientation, turning)

            # call move
            self.move(next_cell)

            current_cell = next_cell

        return orientation, goal_cell[0], goal_cell[1]

    def next_move_bfs(self, x, y, orientation, wall_position, maze_state,
                      fifo_queue, cell_parent_map):

        if (maze_state[y][x] == -1):
            # get surrounding cells
            surrounding_cells, remaining_cell_index = self.get_surround(
                x, y, maze_state)

            # get accessible cells
            accessible_cells = self.is_accessible(x, y, wall_position,
                                                  maze_state)

            visited_cell = [
                cell for cell in accessible_cells
                if maze_state[cell[1]][cell[0]] == 1
            ]

            accessible_cells = [
                cell for cell in accessible_cells if cell not in visited_cell
            ]

            for cell in accessible_cells:
                cell_parent_map[(cell[0], cell[1])] = [x, y]
                fifo_queue.append(cell)

            # mark cell as visited
            maze_state[y][x] = 1

            next_cell = fifo_queue.pop(0)

            if (next_cell in accessible_cells):
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
                    key for key, val in remaining_cell_index.items()
                    if val == next_cell
                ][0]

                if (orientation == next_key):
                    turning = 'F'
                elif ((orientation + 1) % 4 == next_key):
                    API.turnRight()
                    turning = 'R'
                elif ((orientation - 1) % 4 == next_key):
                    API.turnLeft()
                    turning = 'L'
                else:
                    API.turnLeft()
                    API.turnLeft()
                    turning = 'B'

                orientation == next_key

                # call updateOrientation
                orientation = self.update_orientation(orientation, turning)

                # call move
                self.move(next_cell)

                return orientation, next_cell[0], next_cell[1]
            else:
                return self.backtrace_bfs(x, y, orientation, wall_position,
                                          maze_state, fifo_queue,
                                          cell_parent_map, next_cell)
        else:
            next_cell = fifo_queue.pop(0)

            return self.backtrace_bfs(x, y, orientation, wall_position,
                                      maze_state, fifo_queue, cell_parent_map,
                                      next_cell)

    def inverse_path(self, shortest):
        inv = []

        for i in range(0, len(shortest) - 1):
            inv.insert(0, shortest[i])

        inv.append([0, 0])

        return inv

    def shortest_path(self, x, y, cell_parent_map, wall_position, maze_state):

        next_cell = [x, y]

        shortest = [next_cell]

        while (True):
            if ((next_cell[0], next_cell[1]) == (0, 0)):
                break

            next_cell = cell_parent_map[(next_cell[0], next_cell[1])]

            # get accessible cells
            accessible_cells = self.is_accessible(0, 0, wall_position,
                                                  maze_state)

            shortest.insert(0, next_cell)
            if (next_cell in accessible_cells):
                break

        return shortest

    def move_shortest(self, x, y, orientation, path, maze_state,
                      wall_position):
        history = [[x, y]]

        while (len(path) > 0):
            wall_position = self.update_walls(x, y, orientation, maze_state,
                                              wall_position)

            next_cell = path.pop(0)

            # get surrounding cells
            surrounding_cells, remaining_cell_index = self.get_surround(
                x, y, maze_state)

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
                key for key, val in remaining_cell_index.items()
                if val == next_cell
            ][0]

            if (orientation == next_key):
                turning = 'F'
            elif ((orientation + 1) % 4 == next_key):
                API.turnRight()
                turning = 'R'
            elif ((orientation - 1) % 4 == next_key):
                API.turnLeft()
                turning = 'L'
            else:
                API.turnLeft()
                API.turnLeft()
                turning = 'B'

            orientation == next_key

            # call updateOrientation
            orientation = self.update_orientation(orientation, turning)

            # call move
            self.move(next_cell)

            x, y = next_cell

            history.append(next_cell)

        return orientation, next_cell[0], next_cell[1]

    #########################
    # initializer functions #
    #########################

    # generate wall_position
    def get_empty_wall_position(self, width, height):
        wall_position = [[0] * width for _ in range(height)]
        return wall_position

    # generate flood
    def get_initial_flood(self, width, height, wall_position):
        flood_zero = [[-1] * width for _ in range(height)]

        for y in range(int(height / 2) - 1, int(height / 2) + 1):
            for x in range(int(width / 2) - 1, int(width / 2) + 1):
                flood_zero[y][x] = 0

        flood = self.floodfill_algorithm(flood_zero, wall_position)

        return flood

    # generate boolean maze_state
    def get_initial_maze_state_bfs(self, width, height):
        maze_state = [[-1] * width for _ in range(height)]

        for y in range(int(height / 2) - 1, int(height / 2) + 1):
            for x in range(int(width / 2) - 1, int(width / 2) + 1):
                maze_state[y][x] = 0

        return maze_state

    def get_initial_maze_state_dfs(self, width, height):
        maze_state = [[-1] * width for _ in range(height)]

        return maze_state

    #########################
    # check state functions #
    #########################

    # check for goal
    def check_goal(self, x, y, flood):
        cell_val = flood[y][x]

        if (cell_val == 0):
            return True
        else:
            False

    def check_goal_dfs(self, x, y, goal):
        if ([x, y] in goal):
            return True
        else:
            False

    # get (x, y) of surrounding cells
    def get_surround(self, x, y, maze_state):
        surrounding_cells = []

        surrounding_cells.append([x, y + 1])  # north
        surrounding_cells.append([x + 1, y])  # east
        surrounding_cells.append([x, y - 1])  # south
        surrounding_cells.append([x - 1, y])  # west

        removed_cells = [
            cell for cell in surrounding_cells
            if (cell[0] < 0 or cell[0] > len(maze_state[0]) -
                1 or cell[1] < 0 or cell[1] > len(maze_state) - 1)
        ]

        remaining_cell_index = {
            i: cell
            for i, cell in enumerate(surrounding_cells)
            if cell not in removed_cells
        }

        surrounding_cells = [
            cell for cell in surrounding_cells if cell not in removed_cells
        ]

        return surrounding_cells, remaining_cell_index

    # check if mouse can move to a cell
    def is_accessible(self, x, y, wall_position, maze_state):
        # get surrounding cells
        surrounding_cells, _ = self.get_surround(x, y, maze_state)

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
    def update_walls(self,
                     x,
                     y,
                     orientation,
                     maze_state,
                     wall_position,
                     color='G'):
        API.setColor(x, y, color)

        L = API.wallLeft()
        R = API.wallRight()
        F = API.wallFront()

        surrounding_cells, remaining_cell_index = self.get_surround(
            x, y, maze_state)

        if (orientation == 0):
            N = F
            E = R
            S = False
            W = L
        elif (orientation == 1):
            N = L
            E = F
            S = R
            W = False
        elif (orientation == 2):
            N = False
            E = L
            S = F
            W = R
        else:
            N = R
            E = False
            S = L
            W = F

        if (N):
            API.setWall(x, y, 'n')
        if (E):
            API.setWall(x, y, 'e')
        if (S):
            API.setWall(x, y, 's')
        if (W):
            API.setWall(x, y, 'w')

        walls_between = []
        for i, val in enumerate([N, E, S, W]):
            if val:
                if remaining_cell_index.get(i):
                    walls_between.append(remaining_cell_index.get(i))

        # update wall_position with walls
        x = x * 2 + 1
        y = y * 2 + 1

        wall_arr = np.array(wall_position)
        wall_width = wall_arr.shape[1] - 1
        wall_height = wall_arr.shape[0] - 1

        for cell in walls_between:
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
            wall_position[wall_height - wall_cell[1]][wall_cell[0]] = 1

        # return updated wall positions
        return wall_position

    # update orientation
    def update_orientation(self, orientation, turn):
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

    # set goal
    def set_goal(self, flood, preset='center', cx=0, cy=0):
        height = len(flood)
        width = len(flood[0])

        # reset all squares
        for y in range(height):
            for x in range(width):
                flood[y][x] = -1

        if (preset == 'center'):
            for y in range(int(height / 2) - 1, int(height / 2) + 1):
                for x in range(int(width / 2) - 1, int(width / 2) + 1):
                    flood[y][x] = 0
        elif (preset == 'topleft'):
            flood[height - 1][0] = 0
        elif (preset == 'topright'):
            flood[height - 1][width - 1] = 0
        elif (preset == 'bottomleft'):
            flood[0][0] = 0
        elif (preset == 'bottomright'):
            flood[0][width - 1] = 0
        elif (preset == 'custom'):
            flood[cy][cx] = 0

        return flood

    ##################
    # move functions #
    ##################

    # next move functions
    def next_move_flood_fill(self, x, y, orientation, wall_position, flood):
        cell_val = flood[y][x]

        # get surrounding cells
        surrounding_cells, remaining_cell_index = self.get_surround(
            x, y, flood)

        # get accessible cells
        accessible_cells = self.is_accessible(x, y, wall_position, flood)

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
            key for key, val in remaining_cell_index.items()
            if val == next_cell
        ][0]

        if (orientation == next_key):
            turning = 'F'
        elif ((orientation + 1) % 4 == next_key):
            API.turnRight()
            turning = 'R'
        elif ((orientation - 1) % 4 == next_key):
            API.turnLeft()
            turning = 'L'
        else:
            API.turnLeft()
            API.turnLeft()
            turning = 'B'

        orientation == next_key

        # call updateOrientation
        orientation = self.update_orientation(orientation, turning)

        # call move
        self.move(next_cell)

        return orientation, next_cell[0], next_cell[1]

    # move
    def move(self, next_cell):
        API.moveForward()
