from loguru import logger


def part1(data):
    contained = 0
    for line in lines:
        left, right = line.strip().split(",")
        llow, lhigh = [int(x) for x in left.split("-")]
        rlow, rhigh = [int(x) for x in right.split("-")]

        if llow < rlow:
            if lhigh >= rhigh:
                contained += 1
        elif llow == rlow:
            contained += 1
        elif rlow < llow:
            if rhigh >= lhigh:
                contained += 1

    return contained

def part2(data):
    overlap = 0
    # let's trade memory space for ease of implementation!
    for line in lines:
        left, right = line.strip().split(",")
        llow, lhigh = [int(x) for x in left.split("-")]
        lset = set(range(llow, lhigh+1))
        rlow, rhigh = [int(x) for x in right.split("-")]
        rset = set(range(rlow, rhigh + 1))
        if len(lset.intersection(rset)) > 0:
            overlap += 1

    return overlap


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