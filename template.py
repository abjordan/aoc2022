from loguru import logger


def part1(data):
    pass

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