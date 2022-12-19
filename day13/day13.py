from loguru import logger

from enum import Enum
from functools import cmp_to_key
from itertools import zip_longest
import json
import re
import sys

sys.setrecursionlimit(9999999)

class Decision(Enum):
    CORRECT = -1
    CONTINUE = 0
    WRONG = 1
    NONE = 4

def pkt_sort_key(left, right):
    dec = pkt_sort(left, right)
    if dec is Decision.CORRECT:
        return -1
    elif dec is Decision.CONTINUE:
        return 0
    elif dec is Decision.WRONG:
        return 1
    else:
        raise ValueError(f"Error comparing {left} vs {right}: {dec}")

def pkt_sort(left, right):
    #logger.debug(f"{left} {right}")

    # if both values are integers:
    #   left <  right --> CORRECT
    #   left == right --> CONTINUE
    #   left >  right --> WRONG
    if type(left) is int and type(right) is int:
        if left < right:
            return Decision.CORRECT
        elif left > right:
            return Decision.WRONG
        else:
            return Decision.CONTINUE

    # if both values are lists:
    #   compare 1st vs 1st, 2nd vs 2nd, etc.
    #   if left is out of elements (and right is not), they're RIGHT
    #   if right is out of elements (and left is not), they're WRONG
    #   if same len and no comaprison completes, CONTINUE
    if type(left) is list and type(right) is list:
        for l, r in zip_longest(left, right, fillvalue=None):
            if l is None and r is not None:
                logger.debug("Left is empty before Right --> CORRECT")
                return Decision.CORRECT
            elif l is not None and r is None:
                logger.debug("Right is empty before Left --> WRONG")
                return Decision.WRONG
            else:
                dec = pkt_sort(l, r)
                if dec is not Decision.CONTINUE:
                    logger.debug("Subcomparison returned {}".format(str(dec)))
                    return dec
        return Decision.CONTINUE
    
    # If exactly one value is an integer:
    #   convert the integer to a list and retry the comparison
    if type(left) is list:
        list_r = [right]
        dec = pkt_sort(left, list_r)
        return dec
    if type(right) is list:
        list_l = [left]
        dec = pkt_sort(list_l, right)
        return dec
    
    raise ValueError("How did we get here??? {} vs {}".format(left, right))

def part1(data):
    pairs = data.split("\n\n")
    index = 0
    correct_pairs = []
    for pair in pairs:
        index += 1
        left, right = pair.split("\n")
        left = json.loads(left)
        right = json.loads(right)
        logger.debug(f"{left} {right}")
        compare = pkt_sort(left, right)
        logger.info(compare)
        if compare is Decision.CORRECT:
            correct_pairs.append(index)

    return sum(correct_pairs)

def part2(data):
    pkts = re.sub("\n\n", "\n", data).split("\n")
    pkts.append("[[2]]")
    pkts.append("[[6]]")
    
    json_pkts = [json.loads(x) for x in pkts]
    
    sorted_pkts = sorted(json_pkts, key=cmp_to_key(pkt_sort_key))

    # Find the index of the [[2]]:
    idx_2 = None
    idx_6 = None
    for i in range(0, len(sorted_pkts)):
        if pkt_sort(sorted_pkts[i], [[2]]) == Decision.CONTINUE:
            idx_2 = i+1
        elif pkt_sort(sorted_pkts[i], [[6]]) == Decision.CONTINUE:
            idx_6 = i+1 
    print(idx_2, idx_6)
    return idx_2 * idx_6

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            data = infile.read()
    else:
        from aocd import data
    
    logger.info("Today's input is {} characters".format(len(data))) 
    logger.info("Answer to part 1 is: {}".format(part1(data)))
    logger.info("Answer to part 2 is: {}".format(part2(data)))