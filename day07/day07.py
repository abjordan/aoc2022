#!/usr/bin/env python3

from collections import deque

from loguru import logger

FILE = 1
DIR = 2

class inode:
    def __init__(self, name, the_type):
        self._parent = None
        self._type = the_type
        self._name = name
        self._size = None
        self._subdirs = {}
        self._files = {}

def print_tree(top, level=0):
    indent = " " * (level * 4)
    print("{}{}".format(indent, top._name))
    for dirname, inode in top._subdirs.items():
        print_tree(inode, level + 1)
    for filename, inode in top._files.items():
        print("{:<16}{:>24}".format(indent + "    " + filename, inode._size))

def parse_output(data):
    output = deque(data)

    root = inode("/", DIR)
    root._parent = root
    current = root
    while len(output) != 0:
        line = output.popleft()
        #logger.debug(line)
        if line.startswith("$"):
            toks = line.strip().split()
            if toks[1] == "ls":
                entry = output.popleft()
                while True:
                    ftoks = entry.split(" ")
                    if ftoks[0] == "dir":
                        name = ftoks[1]
                        d = inode(name, DIR)
                        d._parent = current
                        current._subdirs[name] = d
                    elif ftoks[0] == "$":
                        # Should be a $ command...
                        output.appendleft(entry)
                        break
                    else:
                        # File
                        fsize  = int(ftoks[0])
                        name = ftoks[1]
                        f = inode(name, FILE)
                        f._size = fsize
                        current._files[name] = f

                    # Check to see if we have any files left
                    if len(output) != 0:
                        entry = output.popleft()
                    else:
                        break

            elif toks[1] == "cd":
                target = toks[2]
                if target == "/":
                    current = root
                    #logger.debug("cd to /")
                elif target == "..":
                    if current._parent is not None:
                        current = current._parent
                        #logger.debug("cd ..")
                else:
                    #logger.debug("cd {}".format(target))
                    if target in current._subdirs.keys():
                        current = current._subdirs[target]
            else:
                logger.error("Unknown command '{}'".format(line))
    return root

big_dirs = []

def calculate_size(dirent):
    my_size = sum([x._size for x in dirent._files.values()])
    children_size = 0
    for name, childent in dirent._subdirs.items():
        children_size += calculate_size(childent)
    size = my_size + children_size
    #logger.debug("{} --> {} = {} of files + {} of subdirs".format(
    #    dirent._name, size, my_size, children_size))
    if size < 100000:
        big_dirs.append([size, dirent._name])
    return size

def part1(data):
    root = parse_output(data)
    #print_tree(root)

    for dirname, dirent in root._subdirs.items():
        sz = calculate_size(dirent)

    #logger.debug(big_dirs)
    return sum([x[0] for x in big_dirs])

best_candidate = [999999999999999999, None]

def find_deletion(dirent, target):
    global best_candidate
    my_size = sum([x._size for x in dirent._files.values()])
    children_size = 0
    for name, childent in dirent._subdirs.items():
        children_size += find_deletion(childent, target)
    size = my_size + children_size
    #logger.debug("{} --> {} = {} of files + {} of subdirs".format(
    #    dirent._name, size, my_size, children_size))
    if size > target:
        if best_candidate is None:
            best_candidate = [size, dirent._name]
        elif size < best_candidate[0]:
            best_candidate = [size, dirent._name]

    return size

def part2(data):
    global best_candidate
    max_size = 70000000
    required_size = 30000000
    
    root = parse_output(data)
    current_size = calculate_size(root)
    unused = max_size - current_size
    to_free = required_size - unused
    logger.debug(f"Total size: {current_size}")
    logger.debug(f"Unused size: {unused}")
    logger.debug("Need to free {} bytes".format(to_free))
    find_deletion(root, to_free)
    logger.debug(best_candidate)
    return best_candidate[0]

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
