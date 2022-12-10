from loguru import logger

import numpy as np

def distance(head, tail):
    vec = ( head[0] - tail[0], head[1] - tail[1] )
    return vec, sum(vec)

sign = lambda x: 0 if not x else int(x/abs(x))

def part1(data):
    head = (0, 0)
    tail = (0, 0)

    tail_positions = set()
    tail_positions.add(tail)

    for line in data:
        direction, steps = line.strip().split(" ")

        logger.debug(f" ----------- {direction} {steps} -----------")

        match direction:
            case "L":
                delta = (-1, 0)
            case "R": 
                delta = (1, 0)
            case "U":
                delta = (0, 1)
            case "D":
                delta = (0, -1)
            case _:
                logger.error("Unknown direction: %s", direction)
                return

        for i in range(0, int(steps)):
            head = (head[0] + delta[0], head[1] + delta[1])

            vec, dist = distance(head, tail)
            tail_dx = 0
            tail_dy = 0

            if vec[0] == 0 and abs(vec[1]) > 1:
                tail_dy += sign(vec[1])
            elif vec[1] == 0 and abs(vec[0]) > 1:
                tail_dx += sign(vec[0])
            elif (abs(vec[0]) > 1) or (abs(vec[1]) > 1):
                tail_dx += sign(vec[0])
                tail_dy += sign(vec[1])
            else:
                # Tail doesn't move
                pass

            tail = (tail[0] + tail_dx, tail[1] + tail_dy)
            tail_positions.add(tail)

            logger.debug(f"head: ({head[0]}, {head[1]})\ttail: ({tail[0]}, {tail[1]})\t{vec}")
    return len(tail_positions)

def part2(data):
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            lines = infile.read().split('\n')
    else:
        from aocd import lines
    
    logger.info("Today's input is {} lines".format(len(lines))) 
    logger.info("Answer to part 1 is: {}".format(part1(lines)))
    logger.info("Answer to part 2 is: {}".format(part2(lines)))