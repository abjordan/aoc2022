from loguru import logger

def parse_rucksacks(data):
    sacks = []
    for line in data:
        items = line.strip()
        half = len(items) // 2
        first = items[0:half]
        second = items[half:] 
        sacks.append( [first, second] )
    return sacks

def get_priority(item):
    if ord(item) < 91:
        return (ord(item) - 64 + 26)
    else:
        return (ord(item) - 96)

def part1(data):
    sacks = parse_rucksacks(data)
    prio_sum = 0
    for sack in sacks:
        # Find the items each half has in common
        common = [ x for x in sack[0] if x in sack[1] ]
        priority = get_priority(common[0])
        prio_sum += priority 
    
    return prio_sum

def part2(data):
    import functools
    groups = []
    for i in range(0, len(data) // 3):
        groups.append( data[i*3:(i*3)+3] )

    prio_sum = 0
    for group in groups:
        guys = [ set(x) for x in group ]
        common = functools.reduce(lambda a, b: a.intersection(b), guys)
        #logger.debug("{} --> {} --> {}".format(common, list(common)[0], get_priority(list(common)[0])))
        prio_sum += get_priority(list(common)[0])

    return prio_sum

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
    