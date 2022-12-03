#!/usr/bin/env python3

from loguru import logger

def part1(data):
    acc = 0
    elves = []
    for line in data:
        if line != '':
            acc += int(line)
        else:
            elves.append(acc)
            acc = 0
    elves.append(acc)
    logger.debug("There are {} elves".format(len(elves)))
    logger.info("Elf with most food has {}".format(max(elves)))
    return elves

def part2(data):
    sorted_elves = sorted(elves)
    top_three = sorted_elves[-3:]
    logger.info("Top three elves have {} in total".format(sum(sorted(elves)[-3:])))

if __name__ == "__main__":
    from aocd import lines
    logger.info("Today's input is {} lines".format(len(lines)))
    elves = part1(lines)
    part2(elves)