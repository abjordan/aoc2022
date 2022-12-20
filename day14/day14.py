from loguru import logger

import numpy as np
import time
import re

# Play area is a 2d grid:
#       0..500..inf
#     0
#    ..
#   inf
# Input is some line segments

AIR = "."
ROCK = "█"
SAND = "o"

FELL_OFF = "fell off"
NO_FALL = "no fall"
CAME_TO_REST = "came to rest"

class Board:
    def __init__(self, max_x, max_y):
        # x and y are backward in NumPy, since it's a row-major array
        # instead of a 2D pixel grid
        self.board = np.full((max_y+25, max_x+25), AIR)
        self.max_y = max_y


    def add_line(self, start, end):
        s_x, s_y = start
        e_x, e_y = end
        #print(f"{start} --> {end}")
        
        # Columns are the same
        if s_x == e_x:
            if s_y < e_y:
                for y in range(s_y, e_y + 1):
                    self.board[y][s_x] = ROCK
            else:
                for y in range(s_y, e_y -1, -1):
                    self.board[y][s_x] = ROCK
        elif s_y == e_y:
            if s_x < e_x:
                for x in range(s_x, e_x + 1):
                    self.board[s_y][x] = ROCK
            else:
                for x in range(s_x, e_x -1, -1):
                    self.board[s_y][x] = ROCK
        else:
            logger.error(f"I don't understand how to draw {start} --> {end}")

    def drop(self):
        # add a stone at 500,0
        sand_x, sand_y = (500,0)
        self.board[sand_y][sand_x] = SAND
        #print(self)

        stopped = False
        while sand_y <= self.max_y:
            #print(self)
            #time.sleep(0.01)
            if self.board[sand_y + 1][sand_x] == AIR:
                self.board[sand_y + 1][sand_x] = SAND
                self.board[sand_y][sand_x] = AIR
                sand_y += 1
            elif self.board[sand_y + 1][sand_x - 1] == AIR:
                self.board[sand_y + 1][sand_x - 1] = SAND
                self.board[sand_y][sand_x] = AIR
                sand_y += 1
                sand_x -= 1
            elif self.board[sand_y + 1][sand_x + 1] == AIR:
                self.board[sand_y + 1][sand_x + 1] = SAND
                self.board[sand_y][sand_x] = AIR
                sand_y += 1
                sand_x += 1
            else:
                #logger.debug("Came to rest")
                stopped = True
                break
        
        if stopped:
            if sand_y == 0 and sand_x == 500:
                return NO_FALL
            else:
                return CAME_TO_REST
        else:
            return FELL_OFF
            

    def __str__(self):
        ret = ""
        for y in range(0, self.max_y+10):
            row = "{:03d} ".format(y)
            for x in range(475, 525):
                row += self.board[y][x]
            row += "\n"
            ret += row
        return ret


def make_grid(data, max_x, max_y):
    grid = Board(max_x, max_y)
    
    for line in lines:
        last = None
        for point in re.split(arrow, line):
            x,y = [int(x) for x in point.split(",")]
            if last is None:
                last = (x, y)
            else:
                grid.add_line(last, (x, y))
                last = (x,y)
    return grid

def part1(data, max_x, max_y):
    grid = make_grid(data, max_x, max_y)
    #print(grid)
    count = 0
    while grid.drop() != FELL_OFF:
        count += 1

    #print(grid)
    return count

def part2(data, max_x, max_y):
    grid = make_grid(data, 1000, max_y)

    # Add a floor: 0,max_y+2 --> 1000,max_y+2
    grid.add_line((0,max_y+2), (1000,max_y+2))
    count = 1
    result = grid.drop()
    while result != NO_FALL:
        count += 1
        result = grid.drop()
    return count

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            lines = infile.read().split('\n')
    else:
        from aocd import lines
    
    arrow = re.compile(r" -> ")
    xs = []
    ys = []
    for line in lines:
        for point in re.split(arrow, line):
            x,y = [int(x) for x in point.split(",")]
            xs.append(x)
            ys.append(y)

    logger.debug(f"x range: {min(xs)} --> {max(xs)}")
    logger.debug(f"y range: {min(ys)} --> {max(ys)}")

    logger.info("Today's input is {} lines".format(len(lines))) 
    logger.info("Answer to part 1 is: {}".format(part1(lines, max(xs), max(ys))))
    logger.info("Answer to part 2 is: {}".format(part2(lines, max(xs), max(ys))))