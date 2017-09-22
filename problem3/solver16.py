# put your 15 puzzle solver here!
from __future__ import division
import random
import Queue as Q


class puzzle_15:

    def __init__(self):
        self.zero = [0,0]
        self.initial_puzzle = [[1, 2, 4, 3], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        self.puzzle_num = random.sample(range(16), 16)
        self.initial_puzzle = [self.puzzle_num[i:i + 4] for i in xrange(0, len(self.puzzle_num), 4)]
        self.goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

    def heuristic(self,puzzle):
        count = 0
        for i in range(4):
            for j in range(4):
                if puzzle[i][j] != self.goal_state[i][j]:
                    count += 1
        return (count/3)

    def is_goal(self,puzzle):
        return puzzle == self.goal_state

    def find_empty(self,puzzle):
        for row in range(4):
            for col in range(4):
                if puzzle[row][col] == 0:
                    return row, col

    def move(self, puzzle, direction, size):
        puzzle_temp = puzzle
        if direction == 'L':
            if size == 1:
                puzzle_temp[self.zero[0]][self.zero[1]] = puzzle_temp[self.zero[0]][self.zero[1]+1]
                puzzle_temp[self.zero[0]][self.zero[1]+1] = 0
                self.zero = [self.zero[0],self.zero[1]+1]
            elif size == 2:
                puzzle_temp[self.zero[0]][self.zero[1]] = puzzle_temp[self.zero[0]][self.zero[1]+1]
                puzzle_temp[self.zero[0]][self.zero[1]+1] = puzzle_temp[self.zero[0]][self.zero[1]+2]
                puzzle_temp[self.zero[0]][self.zero[1]+2] = 0
                self.zero = [self.zero[0], self.zero[1] + 2]

            elif size == 3:
                puzzle_temp[self.zero[0]][self.zero[1]] = puzzle_temp[self.zero[0]][self.zero[1]+1]
                puzzle_temp[self.zero[0]][self.zero[1]+1] = puzzle_temp[self.zero[0]][self.zero[1]+2]
                puzzle_temp[self.zero[0]][self.zero[1]+2] = puzzle_temp[self.zero[0]][self.zero[1]+3]
                puzzle_temp[self.zero[0]][self.zero[1]+3] = 0
                self.zero = [self.zero[0], self.zero[1] + 3]


        elif direction == 'R':
            if size == 1:
                puzzle_temp[zero[0]][0] = puzzle_temp[zero[0]][1]
                puzzle_temp[zero[0]][1] = 0
            elif size == 2:
                puzzle_temp[zero[0]][0] = puzzle_temp[zero[0]][1]
                puzzle_temp[zero[0]][1] = puzzle_temp[zero[0]][2]
                puzzle_temp[zero[0]][2] = 0
            elif size == 3:
                puzzle_temp[zero[0]][0] = puzzle_temp[zero[0]][1]
                puzzle_temp[zero[0]][1] = puzzle_temp[zero[0]][2]
                puzzle_temp[zero[0]][2] = puzzle_temp[zero[0]][3]
                puzzle_temp[zero[0]][3] = 0
        elif direction == 'U':
            temp = tempArr[0][i]
            tempArr[0][i] = tempArr[1][i]
            tempArr[1][i] = tempArr[2][i]
            tempArr[2][i] = tempArr[3][i]
            tempArr[3][i] = temp
        elif direction == 'D':
            temp = tempArr[3][i]
            tempArr[3][i] = tempArr[2][i]
            tempArr[2][i] = tempArr[1][i]
            tempArr[1][i] = tempArr[0][i]
            tempArr[0][i] = temp
        return tempArr


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

    def print_puzzle(puzzle):
        for i in puzzle:
            print i
        print "\n"



print read_puzzle('sample.txt')
print is_goal(read_puzzle('sample.txt'))
# fringe = Q.PriorityQueue()
# fringe.put((1,'new'),(2,'new2'))
# print fringe.get(2)
# print fringe

# #initial_puzzle = [[1,2,4,3],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
#
# print initial_puzzle
# print heuristic(initial_puzzle)
#
# def successors(board):
#     return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]
#
# def successors2(board):
#     state = []
#     # for r in range(N):
#     #     if count_on_row(board, r) == 0:
#     #         for c in range(N):
#     #             if count_on_col(board, c) == 0:
#     #                 state.append(add_piece(board, r, c))
#     #     else:
#     #         continue
#     r = 0
#     c = 0
#     while r < N and count_on_row(board, r) == 0:
#         while c <N and count_on_col(board, c) == 0:
#             state.append(add_piece(board, r, c))
#             #print state
#             c +=1
#         else:
#             c +=1
#             pass
#         r += 1
#         c = 0
#     else:
#         r+=1
#         c = 0
#         pass
#     return state
#
#
#
#
#
# # BFS
# def solve2(initial_board):
#     fringe = [initial_board]
#     while len(fringe) > 0:
#         for s in successors2( fringe.pop(0) ):
#             if is_goal(s):
#                 return(s)
#             fringe.append(s)
#         #print fringe
#     return False
