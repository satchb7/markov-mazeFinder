# Author: Satch Baker
# Class: COSC76 20F
# Professor: Quattrini Li
# Date: November 5th, 2020

import random
import copy
from Maze import Maze

class Robot:
    def __init__(self, startlocation, maze):
        self.location = startlocation
        self.maze = maze

    
    # discussed with dan dipietro '22 about doing the randomization removing from a list
    def getcolor(self):
        allcolors = ["R", "G", "B", "Y"]
        truecolor = self.maze.find_color(self.location[1], self.location[0])
        print(self.location)
        print(truecolor)
        allcolors.remove(truecolor)

        num = random.random()
        if num <= .88:
            return truecolor
        else:
            rand = int(random.random() * len(allcolors))
            misread = allcolors[rand]
            return misread

    def next_moves(self, position):
        # iterate through the possible moves, generating the next states and adding them to the next moves list if they are valid
        # if the move isn't valid, add the original spot
        moves = [(0,1), (1,0), (-1,0), (0,-1)]
        nextstates = []
        for move in moves:
            nextspot = copy.deepcopy(list(position))
            nextspot[0] += move[0]
            nextspot[1] += move[1]
            if not self.maze.is_floor(nextspot[0], nextspot[1]):
                nextstates.append(copy.deepcopy(position))
            else:
                nextstates.append(tuple(nextspot))

        return nextstates
    
    # does the same thing as next_moves, except also moves the robot randomly to one of the possible next moves
    def move(self):
        moves = [(0,1), (1,0), (-1,0), (0,-1)]
        nextstates = []
        # print(position)
        for move in moves:
            nextspot = copy.deepcopy(list(self.location))
            nextspot[0] += move[0]
            nextspot[1] += move[1]
            # print(nextspot)
            if not self.maze.is_floor(nextspot[0], nextspot[1]):
                # print('not valid')
                nextstates.append(tuple(copy.deepcopy(self.location)))
            else:
                # print('valid')
                nextstates.append(tuple(nextspot))

        rand = int(random.random() * len(nextstates))
        chosen = nextstates[rand]
        self.location = chosen


test_maze = Maze("Maze1.maz")
erv = Robot((0,0), test_maze)
print(erv.next_moves((3,2)))
# print(erv.getcolor())
# erv.move()