# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 21:58:55 2021

@authors: GÜVEN ADAL
          BATUHAN BUDAK
          CANKAT ANDAY KADİM
          FURKAN AHİ
"""
import random
import numpy as np
import PySimpleGUI as sg
from queue import Queue
import sys

# State Class
class PuzzleState(object):
    # Constructor(state)
    def __init__(self, blanklocation1, blanklocation2, array):
        self.coloumn = 4
        self.row = 4
        self.blankLocation = (blanklocation1, blanklocation2)
        self.array = array
        self.parent = None

    # Checks if the given state is goal or not
    def isgoal(self):
        goal = np.array([[1, 2, 3, 4], [2, 3, 4, 3], [3, 4, 3, 2], [4, 3, 2, 0]])
        goalState = PuzzleState(3,3,goal)

        if np.array_equal(self.array, goalState.array):
            return True
        else:
            return False

    # Finds the blank space in matrix and returns its location
    def blankfinder(self):
        place = np.where(self.array == 0)
        return place

    # Returns depth of the given state
    def getDepth(self):
        state = self

        depth = 0
        while state.parent is not None:

            depth += 1
            state = state.parent
        return depth

    # Heuristic function ranks alternatives in search algorithm decide which branch to follow
    def hfunc(self):
        info2 = np.zeros((4, 4)) #Creating arrays
        info4 = np.zeros((4, 4))
        info3 = np.zeros((6, 6))
        goal = np.array([[1, 2, 3, 4], [2, 3, 4, 3], [3, 4, 3, 2], [4, 3, 2, 0]])    #Goal is initialized for randomization
        y2 = np.where(goal == 2)  # goal indexes Checking the index of 2
        y2Row = y2[0]
        y2Col = y2[1]
        y3 = np.where(goal == 3)  # goal indexes Checking the index of 3
        y3Row = y3[0]
        y3Col = y3[1]
        y4 = np.where(goal == 4)  # goal indexes Checking the index of 3
        y4Row = y4[0]
        y4Col = y4[1]
        x1 = np.where(self.array == 1) # h function looks at the current state and checks the similarity between the state and the goal state.
        len1 = x1[0] + x1[1]           # This achived by looking at elements of the array and comparing the indexes for each 1 2 3 and 4
        x2 = np.where(self.array == 2)
        x2Row = x2[0]  # row locations
        x2Col = x2[1]  # coloumn locations
        x3 = np.where(self.array == 3)
        x3Row = x3[0]  # row locations
        x3Col = x3[1]  # coloumn locations
        x4 = np.where(self.array == 4)
        x4Row = x4[0]  # row locations
        x4Col = x4[1]  # coloumn locations
        uu = 0
        #Here we are creating a Matrix which we held the distance between the goal and the current locations
        for i in range(0, 4):
            for k in range(0, 4):
                info2[i, k] = abs(y2Row[k] - x2Row[i]) + abs(y2Col[k] - x2Col[i])
        diag = np.trace(info2)#first considering the diagonal of the matrix as first choice then trying to find a betteer choice

        #print(info2)
        min2 = [0, 1, 2, 3]
        #print("111111", min2)
        for i in range(0, 4):
            for k in range(0, 4):# After creating the distance matrix which has the distance of each element 2 for and its distinct distance to all possible rigt locations
                for j in range(0, 4):# This way we are not considering only one location which can fit 2 but all locations and trying to choose between the state which minimize the distance
                    for p in range(0, 4):
                        if ((i != k) and (k != j) and (j != p) and (i != j) and (i != p) and (k != p)): #Because each row of  the distance matrix represents 1 distinct element two out of 4 and coloumns represents
                            if (info2[0, i] + info2[1, k] + info2[2, j] + info2[3, p] < diag):          # its distance to possible goal locations from distance matrix 4 distances will be chosen but none of them cant be
                                min2 = [i, k, j, p]                                                       # in the same row or coloumn. If statement is used for this reason
                                diag = info2[0, i] + info2[1, k] + info2[2, j] + info2[3, p]

        min2 = np.asarray(min2)
        min2 = min2.astype(int)
        len2 = info2[0, min2[0]] + info2[1, min2[1]] + info2[2, min2[2]] + info2[3, min2[3]] #Anti similarity of places of 2's between the state and goal state expressed as an integer
        #print(min2)
        # 33333333333333333333333
        for i in range(0, 6):
            for k in range(0, 6):
                info3[i, k] = abs(y3Row[k] - x3Row[i]) + abs(y3Col[k] - x3Col[i])
        diag3 = np.trace(info3) #first consideri ng the diagonal of the matrix as first choice then trying to find a betteer choice
        #print(info3)
        min3 = [0, 1, 2, 3, 4, 5]
        #print("111111", min2)
        for i in range(0, 6):
            for k in range(0, 6): # Same procedure is done with 3 this time but distance matrix was 6x6 because there are 6 3's and 6 3 locations
                for j in range(0, 6):
                    for p in range(0, 6):
                        for t in range(0, 6):
                            for h in range(0, 6):
                                if ((i != k) and (k != j) and (j != p) and (i != j) and (i != p) and (k != p) and (    #Because each row of  the distance matrix represents 1 distinct element two out of 4 and coloumns represents
                                        i != t) and (k != t) and (j != t) and (i != h) and (k != h) and (j != h) and ( # its distance to possible goal locations from distance matrix 6 distances will be chosen but none of them cant be
                                        p != h) and (p != t) and (t != h)):                                             # in the same row or coloumn. If statement is used for this reason
                                    uu = uu + 1
                                    if (info3[0, i] + info3[1, k] + info3[2, j] + info3[3, p] + info3[4, t] + info3[
                                        5, h] < diag3):
                                        min3 = [i, k, j, p, t, h]
                                        diag3 = info3[0, i] + info3[1, k] + info3[2, j] + info3[3, p] + info3[4, t] + \
                                                info3[5, h]

        # 444444444444444444444444444444444444444444
        for i in range(0, 4):
            for k in range(0, 4):# Same procedure is done with 3 this time but distance matrix was 6x6 because there are 6 3's and 6 3 locations
                info4[i, k] = abs(y4Row[k] - x4Row[i]) + abs(y4Col[k] - x4Col[i])
        diag4 = np.trace(info4)

        min4 = [0, 1, 2, 3]

        for i in range(0, 4):
            for k in range(0, 4):
                for j in range(0, 4):
                    for p in range(0, 4):
                        if ((i != k) and (k != j) and (j != p) and (i != j) and (i != p) and (k != p)):
                            if (info4[0, i] + info4[1, k] + info4[2, j] + info4[3, p] < diag4):
                                min4 = [i, k, j, p]
                                diag = info4[0, i] + info4[1, k] + info4[2, j] + info4[3, p]

        min4 = np.asarray(min4)
        min4 = min4.astype(int)
        len4 = info4[0, min4[0]] + info4[1, min4[1]] + info4[2, min4[2]] + info4[3, min4[3]]


        min3 = np.asarray(min3)
        min3 = min3.astype(int)
        len3 = info3[0, min3[0]] + info3[1, min3[1]] + info3[2, min3[2]] + info3[3, min3[3]] + info3[4, min3[4]] + \
               info3[5, min3[5]] #Anti similarity of places of 3's between the state and goal state expressed as an integer


        return len4 + len3 + len2 + len1  #antisimilarity number which we retrn in the end of our H function. Smaller this number is a state takes less step to solve


    # Successors function returns children of the given state
    def successors(self):
        children = []

        x = self.blankfinder() # x is the location of blank space

        # left
        if (x[1] != 0):  # if blank space is not at left side of the puzzle
            deneme131 = self.array.copy()
            newState = PuzzleState(x[0], x[1], deneme131)
            newState.parent = self

            newState.array[x[0], x[1]] = newState.array[x[0], x[1] - 1]

            newState.array[x[0], x[1] - 1] = 0
            children.append(newState)

        # right
        if (x[1] != 3):  # if blank space is not at right side of the puzzle
            deneme131 = self.array.copy()
            newState = PuzzleState(x[0], x[1], deneme131)
            newState.parent = self


            newState.array[x[0], x[1]] = newState.array[x[0], x[1] + 1]

            newState.array[x[0], x[1] + 1] = 0
            children.append(newState)

        # up
        if (x[0] != 0):  # if blank space is not at up side of the puzzle
            deneme131 = self.array.copy()
            newState = PuzzleState(x[0], x[1], deneme131)
            newState.parent = self

            newState.array[x[0], x[1]] = newState.array[x[0] - 1, x[1]]

            newState.array[x[0] - 1, x[1]] = 0
            children.append(newState)

        # down
        if (x[0] != 3):  # if blank space is not at down side of the puzzle
            deneme131 = self.array.copy()
            newState = PuzzleState(x[0], x[1], deneme131)
            newState.parent = self

            newState.array[x[0], x[1]] = newState.array[x[0] + 1, x[1]]

            newState.array[x[0] + 1, x[1]] = 0

            children.append(newState)

        return children


    # Draw state and its moves
    def drawState(self,window,stepNo,w,moves):
        # Arranging Locations for steps with respect to step number
        if(stepNo < 8):
            rectangle_x = stepNo*230
            rectangle_y = 25
        elif(stepNo >= 8 and stepNo < 16):
            rectangle_x = 1610 - abs(stepNo -8)*230
            rectangle_y = 200
        elif(stepNo >= 16 and stepNo < 24):
            rectangle_x = (stepNo-16)*230
            rectangle_y = 375
        elif(stepNo >= 24 and stepNo < 32):
            rectangle_x = 1610 - abs(stepNo -24)*230
            rectangle_y = 550
        elif(stepNo >= 32 and stepNo < 40):
            rectangle_x = (stepNo - 32) * 230
            rectangle_y = 725
        else:   # If step no > 40 cannot display so locations are assigned as 1
            rectangle_x = 1
            rectangle_y = 1
        graph = window.Element("graph")
        str1 = "W is equal to " + str(w)
        graph.draw_text(str1, (900, 10))    # Display W for solution
        for i in range(4):
            for j in range(4):
                # Arrange colors to display better
                if(self.array[j][i] == 1):
                    fill_color = "orange"
                elif(self.array[j][i] == 2):
                    fill_color = "lightgreen"
                elif(self.array[j][i] == 3):
                    fill_color = "cyan"
                elif(self.array[j][i] == 4):
                    fill_color = "yellow"
                else:
                    fill_color = "white"
                # Draw squares
                graph.draw_rectangle((rectangle_x + i * 30, rectangle_y + j * 30),
                                     (rectangle_x + (i + 1) * 30, rectangle_y + (j + 1) * 30),
                                     fill_color,
                                     line_color="black")
                if (self.array[j][i] != 0): # If square is not blank the draw number
                    graph.draw_text(int(self.array[j][i]), (rectangle_x + 15 + i * 30, rectangle_y + 15 + j * 30))
                if(not self.isgoal()):  # If self is not goal indicate movement of the next step
                    if(stepNo < 7):
                        graph.DrawImage(filename="arrowRight.png",location=(rectangle_x + 160,rectangle_y + 48))
                        graph.draw_text(moves[stepNo],location=(rectangle_x + 180, rectangle_y + 30))
                        if(stepNo == 0):    # If state is initial write "Initial State" under it
                            graph.draw_text("Initial State",location=(rectangle_x + 60,rectangle_y + 130))
                    elif(stepNo == 7 or stepNo == 15 or stepNo == 23 or stepNo == 31):
                        graph.DrawImage(filename="arrowDown.png",location=(rectangle_x + 48,rectangle_y + 130))
                        graph.draw_text(moves[stepNo], location=(rectangle_x + 85, rectangle_y + 145))
                    elif(stepNo > 7 and stepNo < 16):
                        graph.DrawImage(filename="arrowLeft.png",location=(rectangle_x - 70,rectangle_y + 46))
                        graph.draw_text(moves[stepNo], location=(rectangle_x - 50, rectangle_y + 30))
                    elif(stepNo > 15 and stepNo < 24):
                        graph.DrawImage(filename="arrowRight.png", location=(rectangle_x + 160, rectangle_y + 48))
                        graph.draw_text(moves[stepNo], location=(rectangle_x + 180, rectangle_y + 30))
                    elif(stepNo > 23 and stepNo < 32):
                        graph.DrawImage(filename="arrowLeft.png", location=(rectangle_x - 70, rectangle_y + 46))
                        graph.draw_text(moves[stepNo], location=(rectangle_x - 50, rectangle_y + 30))
                    elif(stepNo > 31 and stepNo < 40):
                        graph.DrawImage(filename="arrowRight.png", location=(rectangle_x + 160, rectangle_y + 48))
                        graph.draw_text(moves[stepNo], location=(rectangle_x + 180, rectangle_y + 30))
                else:   # If state is goal write "GOAL" under it
                    graph.draw_text("GOAL",location=(rectangle_x + 60,rectangle_y + 130))
        return graph

# Shuffles the 4 x 4 matrix randomly to get a random initial state
# randomizer method starts shuffling from goal state thus inital state created at the end
# is 100 % solveable
def puzzleGenerator():
    goal = np.array([[1, 2, 3, 4], [2, 3, 4, 3], [3, 4, 3, 2], [4, 3, 2, 0]])
    initial_state = PuzzleState(3, 3, goal)  # initial state is defined as goal at first
    x = initial_state.blankfinder()
    b = random.randint(10, 20)
    for i in range(0, b):
        x = initial_state.blankfinder()  # x is the location of blank space in the puzzle
        a = random.randint(1, 4)  # Creates random int "a" to decide where the blank space will go
                                  # 1 is up 2 is down 3 is left 4 is right
        # up
        if a == 1:
            if (x[0] != 0):  # if blank space is not at upside of the puzzle
                initial_state.array[x[0], x[1]] = initial_state.array[x[0] - 1, x[1]]
                initial_state.array[x[0] - 1, x[1]] = 0

        # down
        elif a == 2:
            if (x[0] != 3):  # if blank space is not at downside of the puzzle
                initial_state.array[x] = initial_state.array[x[0] + 1, x[1]]
                initial_state.array[x[0] + 1, x[1]] = 0


        # left
        elif a == 3:
            if (x[1] != 0):  # if blank space is not at leftside of the puzzle
                initial_state.array[x] = initial_state.array[x[0], x[1] - 1]
                initial_state.array[x[0], x[1] - 1] = 0


        # right
        elif a == 4:
            if (x[1] != 3):  # if blank space is not at rightside of the puzzle
                initial_state.array[x] = initial_state.array[x[0], x[1] + 1]
                initial_state.array[x[0], x[1] + 1] = 0
    blankLoc = initial_state.blankfinder()

    initial_state.blankLocation = blankLoc  #Set blank location of shuffled state

    return initial_state  # returns shuffled array which will be used as initial state

# Check if two numpy arrays are equal or not (check their values)
def checkEqual(arr1,arr2):

    for i in range(4):
        for j in range(4):
            if(arr1[i][j] != arr2[i][j]):
                return True;

    return False

# Initialize window with given title
def window_init(title):

    # Initialize layout
    layout = [
        [
            sg.Graph(
                canvas_size=(1850, 950),
                graph_bottom_left=(0, 950),
                graph_top_right=(1850, 0),
                key="graph"
            )
        ]
    ]
    window = sg.Window(title, layout)
    window.Finalize()
    return window

# Beam Search algorithm
def beamSearch(w, initial_state): # Takes w and initial_state as param

    explored = [] # Explored arr to keep visited nodes
    queue = []
    children = []
    queue.append(initial_state) # Append root state to queue
    cur_depth = -1
    while True:
        while queue:    # While queue is not empty
            state = queue.pop() # pop element from queue

            if(state.getDepth() > cur_depth):   # Get depth of the node if changed
                cur_depth = state.getDepth()    # Set depth of the node as current
                #("Depth: ", cur_depth)
            explored.append(state)  # Append visited state to explored arr
            if(state.isgoal()): # If state is goal then return
                return state
            for child in state.successors():    # Get all children of the state
                if child not in children:   # Add child if it is not in children
                    children.append(child)
        # End of while queue loop ----> Finds all children from current depth then moves on

        # If length of children > w
        if len(children) > w:
            while len(children) > w: # While length of children > w
                max = -1    # set max as -1 at first
                indexOfMax = -1 # set indexOfMax as -1 at first
                for i in range(len(children)):  # loop through children []
                    if children[i].hfunc() > max: # calling h function which calculates similarty of the given state with goal state
                        max = children[i].hfunc()   # if returned value is bigger than max it is new max
                        indexOfMax = i  # Get index of max
                children.pop(indexOfMax) # Remove state with maximum h value from childrens
            # End of while len(children) > w loop ----> it contiunes until there is w states left in children []
        # If children [] is empty it means search algorithm couldn't find solution with curent W so it needs to update it
        if(len(children) == 0):
            print("----W updated: ",w + 1, " ----")
            return None # To update w simply returns None and Program calls beamSearch again with same state, but w = w + 1
        for child in children:
            check = True    # set check as true
            for exp in explored:
                if(not checkEqual(exp.array,child.array)): # If child is in explored []
                    check = False                          # Assign check as False
            if(check):# If check = True
                queue.append(child)     # Append child to queue
                explored.append(child)  #Append child to explored

        children.clear()    # clear children at the end because depth will increase

# Calculates movements and add them into a list
# Calls drawState function in a loop to display solution path
def drawSolution(path,w,window):
    ok = "null"
    a = []
    for i in range(len(path)):
        if (i > 0):
            c = np.where(path[i - 1].array == 0)
            d = np.where(path[i].array == 0)
            ##right
            if (d[1] > c[1]):
                if (path[i - 1].array[d] == 1):
                    ok = "1 left"
                    a.append(ok)
                if (path[i - 1].array[d] == 2):
                    ok = "2 left"
                    a.append(ok)
                if (path[i - 1].array[d] == 3):
                    ok = "3 left"
                    a.append(ok)
                if (path[i - 1].array[d] == 4):
                    ok = "4 left"
                    a.append(ok)

            if (d[1] < c[1]):
                if (path[i - 1].array[d] == 1):
                    ok = "1 right"
                    a.append(ok)
                if (path[i - 1].array[d] == 2):
                    ok = "2 right"
                    a.append(ok)
                if (path[i - 1].array[d] == 3):
                    ok = "3 right"
                    a.append(ok)
                if (path[i - 1].array[d] == 4):
                    ok = "4 right"
                    a.append(ok)

            if (d[0] > c[0]):
                if (path[i - 1].array[d] == 1):
                    ok = "1 up"
                    a.append(ok)
                if (path[i - 1].array[d] == 2):
                    ok = "2 up"
                    a.append(ok)
                if (path[i - 1].array[d] == 3):
                    ok = "3 up"
                    a.append(ok)
                if (path[i - 1].array[d] == 4):
                    ok = "4 up"
                    a.append(ok)
            if (d[0] < c[0]):
                if (path[i - 1].array[d] == 1):
                    ok = "1 down"
                    a.append(ok)
                if (path[i - 1].array[d] == 2):
                    ok = "2 down"
                    a.append(ok)
                if (path[i - 1].array[d] == 3):
                    ok = "3 down"
                    a.append(ok)
                if (path[i - 1].array[d] == 4):
                    ok = "4 down"
                    a.append(ok)
    for i in range(len(path)):
        path[i].drawState(window, i, w,a)

# ------------------------------MAİN-------------------------------

# Creating 3 distinct states
while True:
    s1 = puzzleGenerator()
    s2 = puzzleGenerator()
    s3 = puzzleGenerator()
    if (not (s1.isgoal() and s2.isgoal() and s3.isgoal()) and not (np.array_equal(s1.array, s2.array) or np.array_equal(s2.array, s3.array) or np.array_equal(s1.array, s3.array))):

        break
print("-----S1-----")
print(s1.array)
print("------------")
print("-----S2-----")
print(s2.array)
print("------------")
print("-----S3-----")
print(s3.array)
print("------------")



print("----beamSearch for S1 will be executed----")
# Solve S1
w1 = 2
while True:
    solutions1 = beamSearch(w1,s1) # Calling beamSearch algorithm
    if(solutions1 == None): # If couldn't find soultion fow currnet w increment
        w1 += 1
    else:
        path1 = list()  # Create solution path
        path1.append(solutions1)    # Append nodes to solution path
        parent = solutions1.parent
        while parent:
            path1.append(parent)  # Append nodes to solution path
            parent = parent.parent  # Iteration
        path1.reverse()
        if(len(path1) > 40):    # If solution is longer than 40 steps creates new inital state
                                # Because not able to demonstrate 40+ steps in GUI also
            s1 = puzzleGenerator()
        else:
            break


print("----beamSearch for S2 will be executed----")
w2 = 2
# Solve S2
while True:
    solutions2 = beamSearch(w2,s2) # Calling beamSearch algorithm
    if(solutions2 == None): # If couldn't find soultion fow currnet w increment
        w2 += 1
    else:
        path2 = list() # Create solution path
        path2.append(solutions2)
        parent = solutions2.parent
        while parent:
            path2.append(parent) # Append nodes to solution path
            parent = parent.parent # Iteration
        path2.reverse()
        if(len(path2) > 40):    # If solution is longer than 40 steps creates new inital state
                                # Because not able to demonstrate 40+ steps in GUI also
            s2 = puzzleGenerator()
        else:
            break

print("----beamSearch for S3 will be executed----")
w3 = 2
# Solve S3
while True:
    solutions3 = beamSearch(w3,s3) # Calling beamSearch algorithm
    if(solutions3 == None): # If couldn't find soultion fow currnet w increment
        w3 += 1
    else:
        path3 = list() # Create solution path
        path3.append(solutions3)
        parent = solutions3.parent
        while parent:
            path3.append(parent) # Append nodes to solution path
            parent = parent.parent # Iteration
        path3.reverse()
        if(len(path3) > 40):    # If solution is longer than 40 steps creates new inital state
                                # Because not able to demonstrate 40+ steps in GUI also
            s3 = puzzleGenerator()
        else:
            break

window1 = window_init("Sym-15 Puzzle, Hw2, S1")  # To display solution of S1
window2 = window_init("Sym-15 Puzzle, Hw2, S2")  # To display solution of S2
window3 = window_init("Sym-15 Puzzle, Hw2, S3")  # To display solution of S3

drawSolution(path1,w1,window1)  # Draw solution for S1

drawSolution(path2,w2,window2)  # Draw solution for S2

drawSolution(path3,w3,window3)  # Draw solution for S3

window1.read()
window2.read()
window3.read()


