x = 10

# print(x + 2)

my_string = 'lu hou yang'

# print(my_string)

my_float = 3.142

# print(my_float)

my_bool = True

# print(my_bool)

my_list = [1, 1.25, 'hi', False]

# print(my_list[2])

my_list = [1, 2, 3, 4, 5]

# print(my_list[0])

my_list = [
    [1, 2],
    [3, 4],
    [5, 6],
]

# print(my_list[1][0])

my_dict = {
    'key': 40,
    'k2': 50,
    'k3': 60,
}

# print(my_dict)

# print(2 * 2 + 3 * 2)
# print(6 * 2 + 8 * 2)
# print(4 * 2 + 3 * 2)
# print(8 * 2 + 2 * 2)
# print(1 * 2 + 2 * 2)
# print(3 * 2 + 6 * 2)


def calc_perimeter(height, width):
    perimeter = height * 2 + width * 2
    return perimeter


# print(calc_perimeter(2, 3))
# print(calc_perimeter(5, 5))

my_int = 4

if (my_int > 4):
    print('Greater than 4')
elif (my_int == 4):
    print('Equal 4')
else:
    print('Less than 4')


def mainConsole(delay=0, algo='floodfill'):
    import time

    #######################
    # initialize variable #
    #######################

    # initialize 'mouse' with ConsoleMouse(delay=delay)
    mouse = ConsoleMouse(delay=delay)

    # initialize 'width' & 'height' of maze to 16
    width = 16
    height = 16

    # initialize starting position of mouse, 'X' & 'Y' to 0
    X = 0
    Y = 0

    # initialize 'wall_position' using mouse.get_empty_wall_position(width * 2 + 1, height * 2 + 1)
    wall_position = mouse.get_empty_wall_position(width * 2 + 1,
                                                  height * 2 + 1)

    # load 'maze' from file using mouse.load_maze_from_file(MAZE_PATH)
    maze = mouse.load_maze_from_file(MAZE_PATH)

    # set 'wall_position = maze'
    wall_position = maze

    # the mouse's orientation
    '''
    orients :
        0- North
        1- East
        2- South
        3- West
    '''
    # initialize 'orientation' to 0
    orientation = 0

    # initialize 'history' to []
    history = []

    #############################
    # Micromouse Code Floodfill #
    #############################
    '''
    1. IF (algo == 'floodfill):
    2.    INITIALIZE state = 0, flood = mouse.get_initial_flood(width, height, wall_position)
    3.    WHILE (True):
    4.        IF (mouse.check_goal(X, Y, flood)):
    5.          mouse.show_maze(X, Y, orientation, history, wall_position, flood)
    6.          USE IF, ELIF, ELSE to check 'state' and change goal position
    7.            flood = mouse.set_goal(flood, 'goal_position')
    8.          state += 1
    9.          history = []
    10.       ELSE:
    11.         flood = mouse.floodfill_algorithm(flood, wall_position)
    12.         history.append([X, Y])
    13.         orientation, X, Y = mouse.next_move_flood_fill(X, Y, orientation, wall_position, flood)
    '''
    if (algo == 'floodfill'):
        state = 0
        flood = mouse.get_initial_flood(width, height, wall_position)

        while (True):
            # check if at goal
            if (mouse.check_goal(X, Y, flood)):
                mouse.show_maze(X, Y, orientation, history, wall_position,
                                flood)
                if (state == 0):
                    # to bottom right corner
                    flood = mouse.set_goal(flood, 'bottomright')
                elif (state == 1):
                    # to center
                    flood = mouse.set_goal(flood, 'center')
                elif (state == 2):
                    # to top right corner
                    flood = mouse.set_goal(flood, 'topright')
                elif (state == 3):
                    # to center
                    flood = mouse.set_goal(flood, 'center')
                elif (state == 4):
                    # to top left corner
                    flood = mouse.set_goal(flood, 'topleft')
                elif (state == 5):
                    # to starting position, bottom left
                    flood = mouse.set_goal(flood, 'bottomleft')
                elif (state == 6):
                    # shortest path, center
                    flood = mouse.set_goal(flood, 'center')
                else:
                    break

                state += 1
                history = []

            else:
                flood = mouse.floodfill_algorithm(flood, wall_position)

                history.append([X, Y])

                # mouse.show_maze(X, Y, orientation, history, wall_position,
                #                 flood)

                orientation, X, Y = mouse.next_move_flood_fill(
                    X, Y, orientation, wall_position, flood)

                # time.sleep(delay)
                # print()

        #######################
        # Micromouse Code DFS #
        #######################
        '''
        1. ELIF (algo == 'dfs):
        2.    INITIALIZE lifo_stack = [], trace_stack = [], cell_parent_map = {},
                        maze_state = mouse.get_initial_maze_state_dfs(width, height, wall_position),
                        goal = [[width / 2 - 1, height / 2], [width / 2, height / 2], [width / 2 - 1, height / 2 - 1], [width / 2, height / 2 - 1]]
        3.    WHILE (True):
        4.        IF (mouse.check_goal_dfs(X, Y, goal)):
        5.          mouse.show_maze(X, Y, orientation, history, wall_position, maze_state)
        6.          srt_prt = mouse.shortest_path(X, Y, cell_parent_map, wall_position, maze_state)
        7.          shortest = mouse.shortest_path(X, Y, cell_parent_map, wall_position, maze_state)
        8.          inv = mouse.inverse_path(shortest)
        9.          orientation, X, Y = mouse.move_shortest(X, Y, orientation, inv, maze_state, wall_position)
        10.         mouse.show_maze(X, Y, orientation, srt_prt, wall_position, maze_state)
        11.         orientation, X, Y = mouse.move_shortest(X, Y, orientation, shortest, maze_state, wall_position)
        12.         mouse.show_maze(X, Y, orientation, srt_prt, wall_position, maze_state)
        13.         history = []
        14.         break
        15.      ELSE:
        16.        history.append([X, Y])
        17.        orientation, X, Y = mouse.next_move_dfs(
                        X,
                        Y,
                        orientation,
                        wall_position,
                        lifo_stack,
                        trace_stack,
                        maze_state,
                        history,
                        cell_parent_map
                    )
        '''
    elif (algo == 'dfs'):
        lifo_stack = []
        trace_stack = []
        cell_parent_map = {}

        maze_state = mouse.get_initial_maze_state_dfs(width, height)

        goal = [[width / 2 - 1, height / 2], [width / 2, height / 2],
                [width / 2 - 1, height / 2 - 1], [width / 2, height / 2 - 1]]

        while (True):
            # check if at goal
            if (mouse.check_goal_dfs(X, Y, goal)):

                mouse.show_maze(X, Y, orientation, history, wall_position,
                                maze_state)

                srt_prt = mouse.shortest_path(X, Y, cell_parent_map,
                                              wall_position, maze_state)
                shortest = mouse.shortest_path(X, Y, cell_parent_map,
                                               wall_position, maze_state)
                inv = mouse.inverse_path(shortest)

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, inv, maze_state, wall_position)
                mouse.show_maze(X, Y, orientation, srt_prt, wall_position,
                                maze_state)

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, shortest, maze_state, wall_position)
                mouse.show_maze(X, Y, orientation, srt_prt, wall_position,
                                maze_state)

                history = []
                break

            else:
                history.append([X, Y])

                # mouse.show_maze(X, Y, orientation, history, wall_position,
                #                 maze_state)

                orientation, X, Y = mouse.next_move_dfs(
                    X, Y, orientation, wall_position, lifo_stack, trace_stack,
                    maze_state, history, cell_parent_map)

                # time.sleep(delay)
                # print()

        #######################
        # Micromouse Code BFS #
        #######################
        '''
        1. ELIF (algo == 'bfs):
        2.    INITIALIZE fifo_queue = [], shortest = [], cell_parent_map = {},
                        maze_state = mouse.get_initial_maze_state_bfs(width, height, wall_position),
        3.    WHILE (True):
        4.        IF (mouse.check_goal(X, Y, maze_state)):
        5.          srt_prt = mouse.shortest_path(X, Y, cell_parent_map, wall_position, maze_state)
        6.          shortest = mouse.shortest_path(X, Y, cell_parent_map, wall_position, maze_state)
        7.          inv = mouse.inverse_path(shortest)
        8.          orientation, X, Y = mouse.move_shortest(X, Y, orientation, inv, maze_state, wall_position)
        9.          mouse.show_maze(X, Y, orientation, srt_prt, wall_position, maze_state)
        10.         orientation, X, Y = mouse.move_shortest(X, Y, orientation, shortest, maze_state, wall_position)
        11.         mouse.show_maze(X, Y, orientation, srt_prt, wall_position, maze_state)
        12.         break
        13.      ELSE:
        14.        history.append([X, Y])
        15.        orientation, X, Y = mouse.next_move_bfs(
                        X,
                        Y,
                        orientation,
                        wall_position,
                        maze_state,
                        fifo_queue,
                        cell_parent_map,
                    )
        '''
    elif (algo == 'bfs'):
        fifo_queue = []
        shortest = []
        cell_parent_map = {}

        maze_state = mouse.get_initial_maze_state_bfs(width, height)

        while (True):
            # check if at goal
            if (mouse.check_goal(X, Y, maze_state)):
                srt_prt = mouse.shortest_path(X, Y, cell_parent_map,
                                              wall_position, maze_state)

                shortest = mouse.shortest_path(X, Y, cell_parent_map,
                                               wall_position, maze_state)

                inv = mouse.inverse_path(shortest)

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, inv, maze_state, wall_position)

                mouse.show_maze(X, Y, orientation, srt_prt, wall_position,
                                maze_state)

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, shortest, maze_state, wall_position)

                mouse.show_maze(X, Y, orientation, srt_prt, wall_position,
                                maze_state)

                break

            else:
                history.append([X, Y])

                # mouse.show_maze(X, Y, orientation, history, wall_position,
                #                 maze_state)

                orientation, X, Y = mouse.next_move_bfs(
                    X,
                    Y,
                    orientation,
                    wall_position,
                    maze_state,
                    fifo_queue,
                    cell_parent_map,
                )

                # time.sleep(delay)
                # print()
