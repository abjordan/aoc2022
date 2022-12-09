#!/usr/bin/env python3

import numpy as np

from loguru import logger


def part1(data):
    # Grid is n x n, and a tree is visible from one perspective
    # if there are only trees shorter than it in the way

    # So the silly thing here is that we can repeat the same
    # task and just rotate the map, rather than have to figure
    # out how to iterate over the grid in each direction
    rows, cols = data.shape
    visible = 0
    
    def count_em(int_data):
        bit_arr = np.zeros(int_data.shape)
        #logger.debug("\n" + str(int_data))
        for i in range(0, rows):
            tallest = -1
            for j in range(0, cols):
                if int_data[i][j] > tallest:
                    bit_arr[i][j] = 1
                    tallest = int_data[i][j]
        return bit_arr

    result = np.zeros(data.shape)
    for i in range(0, 4):
        bit_arr = np.rot90(count_em(np.rot90(data, i)), 4 - i)
        #logger.debug(f"{i}\n" + str(bit_arr))
        result = np.logical_or(result, bit_arr)

    return np.count_nonzero(result)

def part2(data):
    # Boo - I can't figure out a clever way to solve this using the same
    # trick from Part 1.
    rows, cols = data.shape

    scenic_score = np.zeros(data.shape)

    #logger.debug(f"rows = {rows}, cols = {cols}")
    for i in range(0, rows):
        #logger.debug(data[i])
        for j in range(0, cols):
            curr = data[i][j]
            # Left is [i][0:j] -- same row, columns up to j
            left_vis = 0
            for y in range(j-1, -1, -1):
                #logger.debug(f"    [{i}][{y}] = {data[i][y]}")
                if data[i][y] < curr:
                    left_vis += 1
                else:
                    left_vis += 1
                    break
            
            # Right is [i][j+1:] - same row, more columns
            right_vis = 0
            for y in range(j+1, cols):
                #logger.debug(f"    [{i}][{y}] = {data[i][y]}")
                if data[i][y] < curr:
                    right_vis += 1
                else:
                    right_vis += 1
                    break
            
            # Up is [0:i][j] - same columns, rows up to i
            up_vis = 0
            for x in range(i-1, -1, -1):
                #logger.debug(f"    [{x}][{j}] = {data[x][j]}")
                if data[x][j] < curr:
                    up_vis += 1
                else:
                    up_vis += 1
                    break

            # Down is [i+1:][j] - same column, other rows
            down_vis = 0
            for x in range(i+1, rows):
                #logger.debug(f"    [{x}][{j}] = {data[x][j]}")
                if data[x][j] < curr:
                    down_vis += 1
                else:
                    down_vis += 1
                    break

            score = left_vis * right_vis * up_vis * down_vis
            #logger.debug(f"[{i}][{j}] = {left_vis} * {right_vis} * {up_vis} * {down_vis} = {score}")
            scenic_score[i][j] = score

    return np.max(scenic_score)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            lines = infile.read().split('\n')
    else:
        from aocd import lines
    
    data_arr = []
    for line in lines:
        data_arr.append([int(x) for x in line.strip()])
    #logger.debug(data_arr)
    field = np.array(data_arr)

    logger.info("Today's input is {} lines".format(len(lines))) 
    logger.info("Answer to part 1 is: {}".format(part1(field)))
    logger.info("Answer to part 2 is: {}".format(part2(field)))