# put your 15 puzzle solver here!
from __future__ import division
import random
import sys
from Queue import PriorityQueue
import copy




#initial_puzzle = [[1, 2, 4, 3], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
#puzzle_num = random.sample(range(16), 16)
#initial_puzzle = [puzzle_num[i:i + 4] for i in xrange(0, len(puzzle_num), 4)]



def heuristic(puzzle):
    count = 0
    for i in range(4):
        for j in range(4):
            if puzzle[i][j] != goal_state[i][j]:
                count += 1
    return ((count-1)/3)

def is_goal(puzzle):
    return puzzle == goal_state

def find_empty(puzzle):
    for row in range(4):
        for col in range(4):
            if puzzle[row][col] == 0:
                return row, col

def move(puzzle, direction, size):
    zero = find_empty(puzzle)
    if direction == 'L':
        if size == 1:

            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]+1]
            puzzle_temp[zero[0]][zero[1]+1] = 0
            return puzzle_temp
            #zero = [zero[0],zero[1]+1]
        elif size == 2:

            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]+1]
            puzzle_temp[zero[0]][zero[1]+1] = puzzle_temp[zero[0]][zero[1]+2]
            puzzle_temp[zero[0]][zero[1]+2] = 0
            #zero = [zero[0], zero[1] + 2]
            return puzzle_temp

        elif size == 3:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]+1]
            puzzle_temp[zero[0]][zero[1]+1] = puzzle_temp[zero[0]][zero[1]+2]
            puzzle_temp[zero[0]][zero[1]+2] = puzzle_temp[zero[0]][zero[1]+3]
            puzzle_temp[zero[0]][zero[1]+3] = 0
            #zero = [zero[0], zero[1] + 3]
            return puzzle_temp

    elif direction == 'R':

        if size == 1:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]-1]
            puzzle_temp[zero[0]][zero[1]-1] = 0
            #zero = [zero[0],zero[1]-1]
            return puzzle_temp
        elif size == 2:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]-1]
            puzzle_temp[zero[0]][zero[1]-1] = puzzle_temp[zero[0]][zero[1]-2]
            puzzle_temp[zero[0]][zero[1]-2] = 0
            #zero = [zero[0], zero[1] - 2]
            return puzzle_temp

        elif size == 3:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]][zero[1]-1]
            puzzle_temp[zero[0]][zero[1]-1] = puzzle_temp[zero[0]][zero[1]-2]
            puzzle_temp[zero[0]][zero[1]-2] = puzzle_temp[zero[0]][zero[1]-3]
            puzzle_temp[zero[0]][zero[1]-3] = 0
            #zero = [zero[0], zero[1] - 3]
            return puzzle_temp

    elif direction == 'U':
        if size == 1:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]+1][zero[1]]
            puzzle_temp[zero[0]+1][zero[1]] = 0
            #zero = [zero[0]+1,zero[1]]
            return puzzle_temp

        elif size == 2:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]+1][zero[1]]
            puzzle_temp[zero[0]+1][zero[1]] = puzzle_temp[zero[0]+2][zero[1]]
            puzzle_temp[zero[0]+2][zero[1]] = 0
            #zero = [zero[0]+ 2, zero[1]]
            return puzzle_temp

        elif size == 3:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]+1][zero[1]]
            puzzle_temp[zero[0]+1][zero[1]] = puzzle_temp[zero[0]+2][zero[1]]
            puzzle_temp[zero[0]+2][zero[1]] = puzzle_temp[zero[0]+3][zero[1]]
            puzzle_temp[zero[0]+3][zero[1]] = 0
            #zero = [zero[0]+3, zero[1]]
            return puzzle_temp

    elif direction == 'D':
        if size == 1:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]-1][zero[1]]
            puzzle_temp[zero[0]-1][zero[1]] = 0
            #zero = [zero[0]-1,zero[1]]
            return puzzle_temp

        elif size == 2:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]-1][zero[1]]
            puzzle_temp[zero[0]-1][zero[1]] = puzzle_temp[zero[0]-2][zero[1]]
            puzzle_temp[zero[0]-2][zero[1]] = 0
            #zero = [zero[0]-2, zero[1]]
            return puzzle_temp

        elif size == 3:
            puzzle_temp = copy.deepcopy(puzzle)
            puzzle_temp[zero[0]][zero[1]] = puzzle_temp[zero[0]-1][zero[1]]
            puzzle_temp[zero[0]-1][zero[1]] = puzzle_temp[zero[0]-2][zero[1]]
            puzzle_temp[zero[0]-2][zero[1]] = puzzle_temp[zero[0]-3][zero[1]]
            puzzle_temp[zero[0]-3][zero[1]] = 0
            #zero = [zero[0]-3, zero[1]]
            return puzzle_temp


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


def print_puzzle( puzzle):
    for i in puzzle:
        print i
    print "\n"


def successors(puzzle):
    state = []
    direction = ['L','R','U','D']
    for d in direction:
        zero = find_empty(puzzle)
        puzzle_copy = copy.deepcopy(puzzle)
        if d == 'L':
            for size in range(1,3-zero[1]+1):
                state.append(move(puzzle_copy,'L',size))
        elif d == 'R':
            for size in range(1,zero[1]+1):
                state.append(move(puzzle_copy,'R',size))
        elif d == 'U':
            for size in range(1,3-zero[0]+1):
                state.append(move(puzzle_copy,'U',size))
        else:
            for size in range(1,zero[0]+1):
                state.append(move(puzzle_copy,'D',size))
    return state


# BFS
def solve(puzzle):
    dict={}
    g = 0
    h = heuristic(puzzle)
    fringe = PriorityQueue()
    fringe.put((h+g, g,puzzle))
    while not fringe.empty():
        f, g_old, state = fringe.get()
        dict[g]=state
        # print dict
        if is_goal(state):
            return dict
        for s in successors(state):
            h = heuristic(s)
            g = g_old+1
            fringe.put((g + h, g, s))
        # print fringe
    return False


def get_path(dict):
    path=[]
    for i in range(1,len(dict)):
        row = find_empty(dict[i])[0]
        col = find_empty(dict[i])[1]
        direction_vertical = row - find_empty(dict[i-1])[0]
        direction_horizontal = col - find_empty(dict[i-1])[1]
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
# def main():
#     a = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 10, 12], [13, 14, 15, 11]]
#
#     #print a
#     move(a,"L",2)
#     print a

    #print a
    #print p.initial_puzzle
    #successors(initial_puzzle)
    #print p.initial_puzzle
    #print s
    # print p.zero
    # print
    # print p.read_puzzle('sample.txt')
    # print p.is_goal(p.read_puzzle('sample.txt'))


file_directory = 'sample.txt'
initial_puzzle = read_puzzle(file_directory)
#zero = find_empty(initial_puzzle)
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

a = copy.deepcopy(initial_puzzle)
b=solve(a)
#print len(b)
#print get_path(b)

k = [[1, 3, 0, 4], [5, 2, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]]
print get_path(solve(a))
#print get_path(solve(a))
#print initial_puzzle


# if __name__ == '__main__':
#     main()

