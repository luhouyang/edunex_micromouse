###########
# imports #
###########

import API
import sys

#######################
# general mouse class #
#######################


class Mouse():

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

    # next move functions
    def nextMove():
        pass

    # move
    def move():
        pass

    # array/queue state functions
