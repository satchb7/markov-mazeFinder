# Author: Satch Baker
# Class: COSC76 20F
# Professor: Quattrini Li
# Date: November 5th, 2020

from Maze import Maze
import random
from Robot import Robot
import numpy as np
from MyMaze import MyMaze

class RobotMarkovProblem:
    def __init__(self, maze):
        self.maze = maze
        self.robot = None
        self.locationsMap = self.generateMap()
        self.itemMap = self.assign_integers()
        self.transition_matrix = self.generate_transitions()
        self.observation_matrixes = self.generate_all_observations()
        self.probabilities_array = self.generate_probabilites()

    def generateMap(self):
        # generate a map of the locations and their frequencies
        locmap = {}
        floor = []
        for i in range(0, self.maze.width):
            for x in range(0, self.maze.height):
                if self.maze.is_floor(i, x):
                    floor.append((i, x))
                locmap[(i,x)] = 0
        
        rand = int(random.random() * len(floor))
        startloc = floor[rand]
        # initialize a robot at a random place on the floor of the maze
        self.robot = Robot(startloc, self.maze)
        self.maze.robotloc = [startloc[0], startloc[1]]

        # assign an initial uniform distribution for all of the spaces
        for tup in floor:
            locmap[tup] = 1/len(floor)

        return locmap
    
    def assign_integers(self):
        # map each location to an integer, used for indexing in a n * 1 probability matrix and more
        itemMap = {}
        itemNumber = 0
        for i in range(0, self.maze.width):
            for x in range(0, self.maze.height):
                itemMap[(i,x)] = itemNumber
                itemNumber += 1
        
        return itemMap

    def generate_transitions(self):
        # generates transition matrix of probability of going from one spot to another
        matrix = []
        for entry in self.itemMap:
            row = [0 for i in range(0, len(self.itemMap))]
            moves = self.robot.next_moves(entry)
            for move in moves:
                row[self.itemMap[move]] += 1
            # normalize
            for i in range(0, len(row)):
                row[i] = row[i]/4
            matrix.append(row)
        transitionMatrix = np.array(matrix)   

        return transitionMatrix

    def generate_observations(self, color):
        # builds a matrix of observations
        matrix = []
        for entry in self.itemMap:
            row = [0 for i in range(0, len(self.itemMap))]
            if color == self.maze.find_color(entry[0], entry[1]):
                row[self.itemMap[entry]] = 0.88
            else:
                row[self.itemMap[entry]] = 0.04
            matrix.append(row)
        observationMatrix = np.array(matrix)

        return observationMatrix

    def generate_all_observations(self):
        # generates observation matrices for all of the colors that we have
        colors = ["R", "G", "B", "Y"]
        observations = {}
        for entry in colors:
            observations[entry] = self.generate_observations(entry)
        
        return observations

    def generate_probabilites(self):
        # generates an initial n * 1 array, and gives the probability of the robot being at that spot
        probabilities = [0 for i in range(0, len(self.itemMap))]
        for i in range(0, self.maze.width):
            for x in range(0, self.maze.height):
                probabilities[self.itemMap[(i,x)]] = [self.locationsMap[(i,x)]]
        
        probabilities = np.array(probabilities)
        return probabilities

    
    # discussed implementation using matrices with Dan Dipietro '22
    # also had knowledge of working with numpy arrays from cosc74
    def progress_function(self):
        # Move the robot and reset its location in the maze
        self.robot.move()
        self.maze.robotloc = [self.robot.location[1], self.robot.location[0]]
        # make an observation
        observed = self.robot.getcolor()
        # multiply the three matrices together to generate the new probabilities distribution
        result1 = np.matmul(self.observation_matrixes[observed], np.transpose(self.transition_matrix))
        result2 = np.matmul(result1, self.probabilities_array)
        # normalize the entries in the matrix so that they sum to 1
        addAll = result2.sum()
        self.probabilities_array = result2/addAll

    # do the progress function a certain number of times and print the maze and probabilities each time
    def progress_by_steps(self, steps):
        for i in range(0, steps):
            # print(self.probabilities_array)
            self.progress_function()
            self.print_distribution()
            print(self.maze)


    def print_distribution(self):
        strings = []
        for i in range(0, self.maze.width):
            string = ""
            for j in range(0, self.maze.height):
                if (i, j) in self.locationsMap:
                    string = string + " " + str(format(self.probabilities_array[self.itemMap[(i,j)]][0], '.3f'))
                else:
                    string = string + " " + str(format(0, '.3f'))

            strings.append(string)
        strings.reverse()
        for row in strings:
            print(row)


if __name__ == "__main__":
    test_maze = MyMaze("Maze1.maz")
    test_problem = RobotMarkovProblem(test_maze)
    test_problem.progress_function()
    #print(test_problem.probabilities_array)
    test_problem.progress_by_steps(10)
    
        