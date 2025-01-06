# %%
"""
Below if for running in Console
"""


def mainConsole(delay=0, algo='floodfill'):
    import time
    from MOUSE import ConsoleMouse

    #######################
    # initialize variable #
    #######################

    mouse = ConsoleMouse(delay=delay)

    width = 16
    height = 16

    X = 0
    Y = 0

    wall_position = mouse.get_empty_wall_position(width * 2 + 1,
                                                  height * 2 + 1)

    # load maze from file
    # maze = mouse.load_maze_from_file(
    #     '/home/lulu/Desktop/edunex/edunex_micromouse/src/houyang/mazes/AAMC15Maze.txt'
    # )
    maze = mouse.load_maze_from_file(
        'C:/Users/User/Desktop/Python/micromouse/edunex_micromouse/src/houyang/mazes/AAMC15Maze.txt'
    )
    wall_position = maze

    # the mouse's orientation
    '''
    orients :
        0- North
        1- East
        2- South
        3- West
    '''
    orientation = 0

    history = []

    #############################
    # Micromouse Code Floodfill #
    #############################

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

                mouse.show_maze(X, Y, orientation, history, wall_position,
                                flood)

                orientation, X, Y = mouse.next_move_flood_fill(
                    X, Y, orientation, wall_position, flood)

                time.sleep(delay)
                print()

    #######################
    # Micromouse Code DFS #
    #######################

    elif (algo == 'dfs'):
        lifo_stack = []
        cell_parent_map = {}
        trace_stack = []

        maze_state = mouse.get_initial_maze_state_dfs(width, height)

        goal = [[width / 2 - 1, height / 2], [width / 2, height / 2],
                [width / 2 - 1, height / 2 - 1], [width / 2, height / 2 - 1]]

        while (True):
            # check if at goal
            if (mouse.check_goal_dfs(X, Y, goal)):

                mouse.show_maze(X, Y, orientation, history, wall_position,
                                maze_state)

                shortest = mouse.shortest_path(X, Y, cell_parent_map,
                                               wall_position, maze_state)
                inv = mouse.inverse_path(shortest)

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, inv, maze_state, wall_position)
                mouse.show_maze(X, Y, orientation, history, wall_position,
                                maze_state)

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, shortest, maze_state, wall_position)
                mouse.show_maze(X, Y, orientation, history, wall_position,
                                maze_state)

                history = []
                break

            else:
                history.append([X, Y])

                mouse.show_maze(X, Y, orientation, history, wall_position,
                                maze_state)

                orientation, X, Y = mouse.next_move_dfs(
                    X, Y, orientation, wall_position, lifo_stack, trace_stack,
                    maze_state, history, cell_parent_map)
                time.sleep(delay)
                print()

    #######################
    # Micromouse Code BFS #
    #######################

    elif (algo == 'bfs'):
        maze_state = mouse.get_initial_maze_state_bfs(width, height)

        fifo_queue = []
        cell_parent_map = {}
        shortest = []

        while (True):
            # check if at goal
            if (mouse.check_goal(X, Y, maze_state)):
                shortest = mouse.shortest_path(X, Y, cell_parent_map,
                                               wall_position, maze_state)

                inv = mouse.inverse_path(shortest)

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, inv, maze_state, wall_position)

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, shortest, maze_state, wall_position)

                break

            else:
                history.append([X, Y])

                mouse.show_maze(X, Y, orientation, history, wall_position,
                                maze_state)

                orientation, X, Y = mouse.next_move_bfs(
                    X,
                    Y,
                    orientation,
                    wall_position,
                    maze_state,
                    fifo_queue,
                    cell_parent_map,
                )

                time.sleep(delay)
                print()


"""
Below if for running in QT
"""


def mainQT(algo='floodfill'):
    import API
    from MOUSE_MMS import SimulationMouse

    #######################
    # initialize variable #
    #######################

    mouse = SimulationMouse()

    width = 16
    height = 16

    X = 0
    Y = 0

    wall_position = mouse.get_empty_wall_position(width * 2 + 1,
                                                  height * 2 + 1)

    # the mouse's orientation
    '''
    orients :
        0- North
        1- East
        2- South
        3- West 
    '''
    orientation = 0

    history = []

    #############################
    # Micromouse Code Floodfill #
    #############################

    if (algo == 'floodfill'):
        # state of the mouse, tracks the path finding progress
        # 0, 1, 2, 3 for each corner
        # 5, 6, 7 for going to goal, going to start, switch to short path
        state = 0

        shortest_path = []
        flood = mouse.get_initial_flood(width, height, wall_position)

        while (True):
            wall_position = mouse.update_walls(X, Y, orientation, flood,
                                               wall_position)

            # check if at goal
            if (mouse.check_goal(X, Y, flood)):
                # showMazeQT(X, Y, orientation, history, wall_position, flood)

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

                # if (state == 0):
                #     flood = mouse.set_goal(flood, 'bottomleft')
                # elif (state == 1):
                #     flood = mouse.set_goal(flood, 'center')
                # else:
                #     break

                state += 1
                API.clearAllColor()
                history = []

            else:
                flood = mouse.floodfill_algorithm(flood, wall_position)

                history.append([X, Y])

                mouse.show(flood)
                shortest_path = mouse.predict_path_floodfill(
                    X, Y, wall_position, flood, shortest_path, history)

                orientation, X, Y = mouse.next_move_flood_fill(
                    X, Y, orientation, wall_position, flood)

    #######################
    # Micromouse Code DFS #
    #######################

    elif (algo == 'dfs'):
        maze_state = mouse.get_initial_maze_state_dfs(width, height)

        lifo_stack = []
        cell_parent_map = {}
        trace_stack = []

        goal = [[width / 2 - 1, height / 2], [width / 2, height / 2],
                [width / 2 - 1, height / 2 - 1], [width / 2, height / 2 - 1]]

        while (True):
            wall_position = mouse.update_walls(X, Y, orientation, maze_state,
                                               wall_position)

            # check if at goal
            if (mouse.check_goal_dfs(X, Y, goal)):
                shortest = mouse.shortest_path(X, Y, cell_parent_map,
                                               wall_position, maze_state)
                inv = mouse.inverse_path(shortest)

                API.clearAllColor()
                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, inv, maze_state, wall_position)
                API.clearAllColor()
                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, shortest, maze_state, wall_position)

                history = []
                break

            else:
                history.append([X, Y])

                # showMazeQT(X, Y, orientation, history, wall_position, flood)
                mouse.show(maze_state)

                orientation, X, Y = mouse.next_move_dfs(
                    X, Y, orientation, wall_position, lifo_stack, trace_stack,
                    maze_state, history, cell_parent_map)

    #######################
    # Micromouse Code BFS #
    #######################

    elif (algo == 'bfs'):
        maze_state = mouse.get_initial_maze_state_bfs(width, height)

        fifo_queue = []
        cell_parent_map = {}
        shortest = []

        history = []

        while (True):
            wall_position = mouse.update_walls(X, Y, orientation, maze_state,
                                               wall_position)

            # check if at goal
            if (mouse.check_goal(X, Y, maze_state)):
                # showMazeQT(X, Y, orientation, history, wall_position, flood)

                shortest = mouse.shortest_path(X, Y, cell_parent_map,
                                               wall_position, maze_state)

                inv = mouse.inverse_path(shortest)

                API.clearAllColor()

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, inv, maze_state, wall_position)

                API.clearAllColor()

                orientation, X, Y = mouse.move_shortest(
                    X, Y, orientation, shortest, maze_state, wall_position)

                break

            else:
                history.append([X, Y])

                # showMazeQT(X, Y, orientation, history, wall_position, flood)
                mouse.show(maze_state)

                orientation, X, Y = mouse.next_move_bfs(
                    X,
                    Y,
                    orientation,
                    wall_position,
                    maze_state,
                    fifo_queue,
                    cell_parent_map,
                )


def run(mode='qt', algo='floodfill', delay=0.3):
    if (mode == 'qt'):
        mainQT(algo=algo)
    elif (mode == 'console'):
        mainConsole(delay=delay, algo=algo)


if __name__ == '__main__':
    """
    mode = 'console' | 'qt'
    algo = 'floodfill' | 'dfs' | 'bfs'
    """

    run(mode='qt', algo='floodfill', delay=0.075)
# %%
