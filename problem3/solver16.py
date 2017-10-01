# put your 15 puzzle solver here!

# In my understanding, the 15-puzzle question is an extended problem of 8-puzzle. However, in this case, we can move
# 1, 2 or 3 tiles each time with uniform cost.
# One important character of this problem is the initial state could be unsolvable when permutation is odd
#
# The program reads the initial state from a file, then parse it in to a list of lists.
# Eg. [[1, 2, 4, 3], [5, 6, 7, 8], [9, 10, 11, 12], [0, 13, 14, 15]]
#
# The goal states is the canonical configuration of puzzle, which is:
# [[1, 2, 4, 3], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
#
# Valid states include move 1, 2 or 3 tiles in 4 directions -- up, down, left and right
# For example, with the initial state above, we have 6 valid states
# [[1, 2, 4, 3], [5, 6, 7, 8], [9, 10, 11, 12], [13, 0, 14, 15]]
# [[1, 2, 4, 3], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 0, 15]]
# [[1, 2, 4, 3], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
# [[1, 2, 4, 3], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]]
# [[1, 2, 4, 3], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]]
# [[1, 2, 4, 3], [0, 6, 7, 8], [5, 10, 11, 12], [9, 13, 14, 15]]
# [[0, 2, 4, 3], [1, 6, 7, 8], [5, 10, 11, 12], [9, 13, 14, 15]]
#
# The successor function checks the position of blank space(0), then try to move tiles in 4 directions with different
# number of tiles.
# Wherever the blank space is, there are always 6 possible states
#
# The heuristic function is the manhattan distance to the goal state divide by 3. For the regular 15-puzzle,
# manhattan distance is admissible. And for this question, the goal state can be achieved at most
# 3 times faster than the regular one (if we can solve it by moving 3 tiles at a time, and it is the optimal solution).
# Therefore, when it divide by 3, the heuristic value are always less or equal than the minimal moves to goal state.
# Since the division creates decimal points, division module is imported.
#
# Cost function is f = (total moves to a state + heuristic of the state)
#
# How this program works?
# The algorithm #2 is used, and fringe is set as priority queue. Given an initial state, and put it into fringe
# in the form of (f, total moves so far, initial state)
# While the fringe is not empty, get the element with highest priority(lowest cost), and update it into a dictionary.
# (The dictionary update each time a state is taken from fringe, which means when the goal state is met, the dictionary
# will have the optimal path.) Then, check if it is goal. If not put it into CLOSED list.
# Then find its successors and if the successor state is in CLOSED, then we discard it. Otherwise, calculate costs, then put into fringe.
# After finding the optimal solution, we use the dictionary we had in solve process to generate outputs.



from __future__ import division
import random
from Queue import PriorityQueue
import copy
import sys
import math




#initial_puzzle = [[1, 2, 4, 3], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
#puzzle_num = random.sample(range(16), 16)
#initial_puzzle = [puzzle_num[i:i + 4] for i in xrange(0, len(puzzle_num), 4)]


def find_tile(puzzle,tile_num):
    for row in range(4):
        for col in range(4):
            if puzzle[row][col] == tile_num:
                return row, col

# heuristic function
# def heuristic(puzzle):
#     count = 0
#     for i in range(4):
#         for j in range(4):
#             if puzzle[i][j] != goal_state[i][j]:
#                 count += 1
#     return (count-1)/3

# heuristic function
# def heuristic(puzzle):
#     sum = 0
#     tile_num_list = []
#     for num in range(1,16):
#         tile_num_list.append(find_tile(puzzle,num))
#         #print tile_num_list
#     for i in range(0,15):
#         #print tile_num_list[i]
#         for k in range(0,2):
#             #print tile_num_list[i][k]
#             #print goal_state_list[i][k]
#             sum = sum + abs(tile_num_list[i][k]-goal_state_list[i][k])
#     return sum/3

# def heuristic(puzzle):
#     sum = 0
#     tile_num_list = []
#     for num in range(1,16):
#         tile_num_list.append(find_tile(puzzle,num))
#         #print tile_num_list
#     for i in range(0,15):
#         #print tile_num_list[i]
#         for k in range(0,2):
#             #print tile_num_list[i][k]
#             #print goal_state_list[i][k]
#             if tile_num_list[i][k] != goal_state_list[i][k] :
#                 sum +=1
#     return sum/3


def heuristic(puzzle):
    sum = 0
    tile_num_list = []
    for num in range(1,16):
        tile_num_list.append(find_tile(puzzle,num))
        #print tile_num_list
    for i in range(0,15):
        if tile_num_list[i][0] != goal_state_list[i][0] and tile_num_list[i][1] != goal_state_list[i][1]:
            sum += 1
    return sum
    


# check if state is goal state
def is_goal(puzzle):
    return puzzle == goal_state


# find the position of black space
# return the row and col number
def find_empty(puzzle):
    for row in range(4):
        for col in range(4):
            if puzzle[row][col] == 0:
                return row, col


# return a state after move 1, 2 or 3 tiles in 1 of the 4 directions
def move(puzzle, direction, size):
    zero = find_empty(puzzle)
    puzzle_temp = copy.deepcopy(puzzle)
    if direction == 'L':
        if size == 1:


            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]+1]
            puzzle_temp[zero[0]][zero[1]+1] = 0
            return puzzle_temp
            #zero = [zero[0],zero[1]+1]
        elif size == 2:

            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]+1]
            puzzle_temp[zero[0]][zero[1]+1] = puzzle_temp[zero[0]][zero[1]+2]
            puzzle_temp[zero[0]][zero[1]+2] = 0
            #zero = [zero[0], zero[1] + 2]
            return puzzle_temp

        elif size == 3:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]+1]
            puzzle_temp[zero[0]][zero[1]+1] = puzzle_temp[zero[0]][zero[1]+2]
            puzzle_temp[zero[0]][zero[1]+2] = puzzle_temp[zero[0]][zero[1]+3]
            puzzle_temp[zero[0]][zero[1]+3] = 0
            #zero = [zero[0], zero[1] + 3]
            return puzzle_temp

    elif direction == 'R':

        if size == 1:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]-1]
            puzzle_temp[zero[0]][zero[1]-1] = 0
            #zero = [zero[0],zero[1]-1]
            return puzzle_temp
        elif size == 2:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]-1]
            puzzle_temp[zero[0]][zero[1]-1] = puzzle_temp[zero[0]][zero[1]-2]
            puzzle_temp[zero[0]][zero[1]-2] = 0
            #zero = [zero[0], zero[1] - 2]
            return puzzle_temp

        elif size == 3:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]-1]
            puzzle_temp[zero[0]][zero[1]-1] = puzzle_temp[zero[0]][zero[1]-2]
            puzzle_temp[zero[0]][zero[1]-2] = puzzle_temp[zero[0]][zero[1]-3]
            puzzle_temp[zero[0]][zero[1]-3] = 0
            #zero = [zero[0], zero[1] - 3]
            return puzzle_temp

    elif direction == 'U':
        if size == 1:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]+1][zero[1]]
            puzzle_temp[zero[0]+1][zero[1]] = 0
            #zero = [zero[0]+1,zero[1]]
            return puzzle_temp

        elif size == 2:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]+1][zero[1]]
            puzzle_temp[zero[0]+1][zero[1]] = puzzle_temp[zero[0]+2][zero[1]]
            puzzle_temp[zero[0]+2][zero[1]] = 0
            #zero = [zero[0]+ 2, zero[1]]
            return puzzle_temp

        elif size == 3:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]+1][zero[1]]
            puzzle_temp[zero[0]+1][zero[1]] = puzzle_temp[zero[0]+2][zero[1]]
            puzzle_temp[zero[0]+2][zero[1]] = puzzle_temp[zero[0]+3][zero[1]]
            puzzle_temp[zero[0]+3][zero[1]] = 0
            #zero = [zero[0]+3, zero[1]]
            return puzzle_temp

    elif direction == 'D':
        if size == 1:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]-1][zero[1]]
            puzzle_temp[zero[0]-1][zero[1]] = 0
            #zero = [zero[0]-1,zero[1]]
            return puzzle_temp

        elif size == 2:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]-1][zero[1]]
            puzzle_temp[zero[0]-1][zero[1]] = puzzle_temp[zero[0]-2][zero[1]]
            puzzle_temp[zero[0]-2][zero[1]] = 0
            #zero = [zero[0]-2, zero[1]]
            return puzzle_temp

        elif size == 3:
            #puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]-1][zero[1]]
            puzzle_temp[zero[0]-1][zero[1]] = puzzle_temp[zero[0]-2][zero[1]]
            puzzle_temp[zero[0]-2][zero[1]] = puzzle_temp[zero[0]-3][zero[1]]
            puzzle_temp[zero[0]-3][zero[1]] = 0
            #zero = [zero[0]-3, zero[1]]
            return puzzle_temp


# read file and parse into list of lists
def read_puzzle(file_directory):
    puzzle = []
    with open(file_directory, 'rb') as f:
        for item in f:
            element = item.split(" ")
            row = []
            for num in element:
                row.append(int(num))
            puzzle.append(row)
    return puzzle


# successor function
def successors(puzzle):
    state = []
    direction = ['L','R','U','D']
    for d in direction:
        zero = find_empty(puzzle)  # find blank space
        puzzle_copy = copy.deepcopy(puzzle)
        if d == 'L':
            for size in range(1, 3-zero[1]+1):
                state.append(move(puzzle_copy,'L',size))
        elif d == 'R':
            for size in range(1, zero[1]+1):
                state.append(move(puzzle_copy,'R',size))
        elif d == 'U':
            for size in range(1, 3-zero[0]+1):
                state.append(move(puzzle_copy,'U',size))
        elif d == 'D':
            for size in range(1, zero[0]+1):
                state.append(move(puzzle_copy,'D',size))
    return state


# BFS
def solve(puzzle):
    path_dict={}
    closed = []
    g = 0
    path = {}
    h = heuristic(puzzle)
    fringe = PriorityQueue()
    fringe.put((h+g, g, puzzle))
    while not fringe.empty():
        f, g_old, state = fringe.get()

        print f, g_old,state
        #path_dict[g_old] = state

        if is_goal(state):
            #print path
            return path
        else:
            closed.append(state)
        for s in successors(state):
            if s in closed:
                continue
            h = heuristic(s)
            g = g_old+1
            # if str(s) not in path.keys():
            #     path[str(s)] = state
            object = path.get(str(s))
            if not object:
                path[str(s)] = state
            fringe.put((g + h, g, s))

        # print fringe
    return False

def get_path(path, initial_state, goal_state):
    state = goal_state
    path_list = [state]
    while state != initial_state:
        state = path[str(state)]
        path_list.append(state)
    #path_list.append(initial_state)  # optional
    path_list.reverse()  # optional
    #print path_list
    return path_list

def print_path(path_list):
    # print path_dict
    path=[]
    for i in range(1,len(path_list)):
        row = find_empty(path_list[i])[0]
        col = find_empty(path_list[i])[1]
        direction_vertical = row - find_empty(path_list[i-1])[0]
        direction_horizontal = col - find_empty(path_list[i-1])[1]
        #print direction_vertical,direction_horizontal
        if direction_vertical > 0:
            move = 'U' + str(abs(direction_vertical)) + str(col+1)
            path.append(move)
        elif direction_vertical < 0:
            move = 'D' + str(abs(direction_vertical)) + str(col+1)
            path.append(move)
        elif direction_horizontal > 0:
            move = 'L' + str(abs(direction_horizontal)) + str(row+1)
            path.append(move)
        elif direction_horizontal < 0:
            move = 'R' + str(abs(direction_horizontal)) + str(row+1)
            path.append(move)
        #print path

    return ' '.join(path)


def main():
    file_directory = sys.argv[1]
    #file_directory = 'sample.txt'
    initial_puzzle = read_puzzle(file_directory)
    #puzzle_num = random.sample(/Users/Joshua/Documents/CSCI B551/Assignment 1/github/ahnaik-abkanike-cw234-a1/problem3range(16), 16)
    #initial_puzzle = [puzzle_num[i:i + 4] for i in xrange(0, len(puzzle_num), 4)]
    #puzzle_copy = copy.deepcopy(initial_puzzle)


    global goal_state
    global goal_state_list
    goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    goal_state_list = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3),
                       (3, 0), (3, 1), (3, 2)]
    #print get_path(solve(puzzle_copy))
    #print get_path(solve(puzzle_copy), initial_puzzle, goal_state)
    print print_path(get_path(solve(initial_puzzle),initial_puzzle,goal_state))
    print heuristic(initial_puzzle)

if __name__ == '__main__':
    main()

