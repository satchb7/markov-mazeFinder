# Author: Satch Baker
# Class: COSC76 20F
# Professor: Quattrini Li
# Date: November 5th, 2020

import copy

class MyMaze:
    def __init__(self, fileName):
        self.robotloc = []

        self.maze = []
        f = open(fileName, "r")
        for line in f:
            line = line.strip()
            row = []
            for i in range(0, len(line)):
                row.append(line[i])
            self.maze.append(row)
        
        self.maze.reverse()
        f.close()
        self.width = len(self.maze[0])
        self.height = len(self.maze)

    def find_color(self, x, y):
        return self.maze[y][x]

    def is_floor(self, x, y):
        if x < 0 or x >= self.width:
            # print("width violation")
            return False
        if y < 0 or y >= self.height:
            # print("height violation")
            return False

        # print(str(y) + "  is y")
        # print(str(x) + "  is x")
        # print(self.maze[y][x])
        return self.maze[x][y] != "#"
    
    def __str__(self):
        reverse = copy.deepcopy(self.maze)
        reverse[self.robotloc[0]][self.robotloc[1]] = "$"
        reverse.reverse()
        string = ""
        for row in reverse:
            for character in row:
                string = string + character
            string = string + "\n"
        return string

if __name__ == "__main__":
    test_maze1 = MyMaze("Maze1.maz")

