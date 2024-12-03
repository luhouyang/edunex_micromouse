# %%
"""
Below if for running in Console
"""


def mainConsole():
    from MOUSE import ConsoleMouse

    #######################
    # initialize variable #
    #######################

    mouse = ConsoleMouse(algorithm='FLOODFILL')

    width = 16
    height = 16

    wall_position = mouse.get_empty_wall_position(width * 2 + 1,
                                                  height * 2 + 1)

    flood = mouse.get_initial_flood(width, height, wall_position)

    # load maze from file
    # maze = loadMazeFromFile(
    #     '/home/lulu/Desktop/edunex/edunex_micromouse/src/houyang/mazes/AAMC15Maze.txt'
    # )
    maze = mouse.load_maze_from_file(
        'C:/Users/User/Desktop/Python/micromouse/edunex_micromouse/src/houyang/mazes/AAMC15Maze.txt'
    )
    wall_position = maze

    X = 0
    Y = 0

    # the mouse's orientation
    '''
    orients :
        0- North
        1- East
        2- South
        3- West
    '''
    orientation = 0

    ###################
    # Micromouse Code #
    ###################

    history = []

    while (True):
        # check if at goal
        if (mouse.check_goal(X, Y, flood)):
            history = []
            break

        else:
            flood = mouse.floodfill_algorithm(flood, wall_position)

            history.append([X, Y])

            mouse.show_maze(X, Y, orientation, history, wall_position, flood)

            orientation, X, Y = mouse.next_move_flood_fill(
                X, Y, orientation, wall_position, flood)

            print()


"""
Below if for running in QT
"""


def mainQT():
    import API
    from MOUSE_MMS import SimulationMouse

    #######################
    # initialize variable #
    #######################

    mouse = SimulationMouse(algorithm='FLOODFILL')

    width = 16
    height = 16

    wall_position = mouse.get_empty_wall_position(width * 2 + 1,
                                                  height * 2 + 1)

    flood = mouse.get_initial_flood(width, height, wall_position)

    X = 0
    Y = 0

    # state of the mouse, tracks the path finding progress
    # 0, 1, 2, 3 for each corner
    # 5, 6, 7 for going to goal, going to start, switch to short path
    state = 0

    # the mouse's orientation
    '''
    orients :
        0- North
        1- East
        2- South
        3- West 
    '''
    orientation = 0

    ###################
    # Micromouse Code #
    ###################

    shortest_path = []

    history = []

    while (True):
        wall_position = mouse.update_walls_floodfill(X, Y, orientation, flood,
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


if __name__ == '__main__':
    # mainConsole()
    mainQT()
# %%
