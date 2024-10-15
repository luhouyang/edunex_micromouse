###########
# imports #
###########

import API
import sys

##########################
# simulation mouse class #
##########################


class SimulationMouse():

    def __init__(self, algorithm='FLOODFILL'):
        '''
        Acts as a flag to determine state, move, calculation functions
        Available values:
        1) FLOODFILL - FloodFill algorithm
        2) DFS - Depth first search
        3) BSF - Breadth first search
        '''
        self.algorithm = algorithm

    #########
    # utils #
    #########

    # print a message to the mms console
    def log(self, msg):
        sys.stderr.write(f"{msg}\n")

    # reset states
    def reset():
        pass

    # show info on simulator

    #########################
    # check state functions #
    #########################

    # check if mouse can move to a cell

    # check for center

    # get (x, y) of surrounding cells

    ##########################
    # update state functions #
    ##########################

    # update orientation

    # update coordinates

    # update walls

    # append zero to center cells

    # change destination of mouse

    # append destination

    ##################
    # move functions #
    ##################

    # next move functions
    def nextMove():
        pass

    # move
    def move():
        pass

    # shortest path

    # inverse path


##########################
# simulation mouse class #
##########################


class RealMouse():

    def __init__(self, algorithm='FLOODFILL'):
        '''
        Acts as a flag to determine state, move, calculation functions
        Available values:
        1) FLOODFILL - FloodFill algorithm
        2) DFS - Depth first search
        3) BSF - Breadth first search
        '''
        self.algorithm = algorithm

    #########
    # utils #
    #########

    # print a message to the mms console
    def log(self, msg):
        sys.stderr.write(f"{msg}\n")

    # reset states
    def reset():
        pass

    # show info on simulator

    # update orientation

    # update coordinates

    # update walls

    # check if mouse can move to a cell

    # check for center

    # append zero to center cells

    # change destination of mouse

    # append destination

    # get (x, y) of surrounding cells

    # next move functions
    def nextMove():
        pass

    # move
    def move():
        pass

    # shortest path

    # inverse path
