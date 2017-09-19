# put your 15 puzzle solver here!
import random


puzzle_num = random.sample(range(16), 16)
initial_puzzle = [puzzle_num[i:i + 4] for i in xrange(0, len(puzzle_num), 4)]
