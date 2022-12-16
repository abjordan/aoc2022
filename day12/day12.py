#!/usr/bin/env python3

from loguru import logger
from collections import deque

import numpy as np

class Grid:
    def __init__(self, data):
        lines = [list(x) for x in data.split("\n")]
        nums = []
        for line in lines:
            row = []
            for col in line:
                row.append(ord(col))
            nums.append(row)
        self._grid = np.array(nums)
        
        start = np.where(self._grid == ord('S'))
        end = np.where(self._grid == ord('E'))
        self._start = (start[0][0], start[1][0])
        self._end = (end[0][0], end[1][0])
        
        self._grid[self._start] = ord('a')    
        self._grid[self._end] = ord('z')
        print(self._start, self._end)

    def neighbors(self, location):
        '''Neighbors of a location are places where the destination value is less than current height + 1'''
        row, col = location
        valid = []
        me = self._grid[row][col]
        # Up
        if row > 0:
            if self._grid[row-1][col] <= (me + 1): valid.append((row-1, col))
        # Down
        if row < (self._grid.shape[0] - 1):
            if self._grid[row+1][col] <= (me + 1): valid.append((row+1, col))
        # Left
        if col > 0:
            if self._grid[row][col - 1] <= (me + 1): valid.append((row, col-1))
        # Right
        if col < (self._grid.shape[1] - 1):
            if self._grid[row][col + 1] <= (me + 1): valid.append((row, col+1))
        
        return valid
        
    def breadth_first_search(self, start, end):
        frontier = deque()
        frontier.append(start)
        came_from = {}
        came_from[start] = None

        while len(frontier) != 0:
            current = frontier.popleft()
            if current == end:
                break

            for next in self.neighbors(current):
                if next not in came_from:
                    frontier.append(next)
                    came_from[next] = current

        # Reconstruct the path from the came_from list
        if end not in came_from:
            return 9999999999999999

        path = [end]
        curr = end
        while curr != start:
            curr = came_from[curr]
            path.append(curr)

        path.reverse()
        return len(path) - 1

def part1(data):
    g = Grid(data)
    logger.debug(f"Grid is {str(g._grid.shape)}")

    pathlen = g.breadth_first_search(g._start, g._end)
    return pathlen

def part2(data):
    g = Grid(data)

    a_locs = np.argwhere(g._grid == ord('a'))
    logger.debug(f"There are {len(a_locs)} a's")
    
    shortest = 999999999999999999
    for a_loc in a_locs:
        a_loc = (a_loc[0], a_loc[1])
        logger.debug(f"{a_loc}")
        pathlen = g.breadth_first_search(a_loc, g._end)
        if pathlen < shortest:
            shortest = pathlen
            logger.debug(f"{a_loc} ==> {shortest}")
    return shortest


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            data = infile.read()
    else:
        from aocd import data
    
    #logger.info("Today's input is {} lines".format(len(lines))) 
    logger.info("Answer to part 1 is: {}".format(part1(data)))
    logger.info("Answer to part 2 is: {}".format(part2(data)))