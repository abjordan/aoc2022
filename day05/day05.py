#!/usr/bin/env python3

import re

from collections import defaultdict
from loguru import logger

instruction_regex = re.compile(r'move (?P<count>\d+) from (?P<src>\d+) to (?P<dst>\d+)')

def parse_stacks(data):
    stacks = defaultdict(list)
    num_stacks = 1 + len(data[0]) // 4
    #logger.debug(f"Found {num_stacks} stacks")
    instructions = []
    idx = 0
    for line in data:
        # a line that starts with '1' 
        if line.startswith(' 1 '):
            idx += 2  # Skip the blank line
            break
        for i in range(0, num_stacks):
            box = line[(i*4) + 1]
            if box != ' ':
                stacks[i+1].insert(0, box)
        idx += 1
    instructions = data[idx:]
    return stacks, instructions

def part1(data):
    stacks, instructions = parse_stacks(data)
    num_stacks = len(stacks.keys())
    
    for instruction in instructions:
        m = instruction_regex.match(instruction)
        count = int(m.group('count'))
        src = int(m.group('src'))
        dst = int(m.group('dst'))

        for i in range(0, count):
            if len(stacks[src]) != 0:
                tok = stacks[src].pop()
                stacks[dst].append(tok)

    tops = []
    for i in range(1, num_stacks + 1):
        tops.append(stacks[i].pop())
    return ''.join(tops)

def part2(data):
    stacks, instructions = parse_stacks(data)
    num_stacks = len(stacks.keys())
    
    for instruction in instructions:
        m = instruction_regex.match(instruction)
        count = int(m.group('count'))
        src = int(m.group('src'))
        dst = int(m.group('dst'))

        tmp_stack = []
        for i in range(0, count):
            if len(stacks[src]) != 0:
                tok = stacks[src].pop()
                tmp_stack.append(tok)
        for i in range(0, count):
            if len(tmp_stack):
                stacks[dst].append(tmp_stack.pop())

    tops = []
    for i in range(1, num_stacks + 1):
        tops.append(stacks[i].pop())
    return ''.join(tops)


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
