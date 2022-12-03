from loguru import logger

ROCK = 'A'          # 65
PAPER = 'B'         # 66
SCISSORS = 'C'      # 67

PICK_ROCK = 'X'     # 88
PICK_PAPER = 'Y'    # 89
PICK_SCISSORS = 'Z' # 90

NAMES = { ROCK: 'ROCK', PAPER: 'PAPER', SCISSORS: 'SCISSORS',
          PICK_ROCK: 'ROCK', PICK_PAPER: 'PAPER', PICK_SCISSORS: 'SCISSORS' }

# Rock beats scissors, scissors beats paper, paper beats rock

pick_scores = { PICK_ROCK: 1, PICK_PAPER: 2, PICK_SCISSORS: 3 }

def score_round(theirs, mine):
    # Could you have done this with a bunch of if... else statements? Yes.
    # Would it have been faster to type them all than to figure this out? Also yes.
    # Would it have been as intellectually satisfying? /shrug
    diff = ord(mine) - 23 - ord(theirs)
    if diff < 0: diff += 3
    score = pick_scores[mine] + (3 * ((diff + 1) % 3))
    return score

def part1(data):
    total = 0
    for line in data:
        picks = line.strip().split(" ")
        total += score_round(*picks)
    logger.info("Part 1: Total score is {}".format(total))

def part2(data):
    # Now, X means we need to lose, Y means we need to draw, and Z means win
    # Pick the symbol that gives you the right answer, scored otherwise the same
    picks  = { 
        ROCK: { 'X': PICK_SCISSORS, 'Y': PICK_ROCK, 'Z': PICK_PAPER },
        PAPER: { 'X': PICK_ROCK, 'Y': PICK_PAPER, 'Z': PICK_SCISSORS },
        SCISSORS: { 'X': PICK_PAPER, 'Y': PICK_SCISSORS, 'Z': PICK_ROCK }
    }

    total = 0
    for line in data:
        theirs, outcome = line.strip().split(" ")
        total += score_round(theirs, picks[theirs][outcome])
    logger.info("Part 2: Total score is {}".format(total))

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            lines = infile.read().split('\n')
    else:
        from aocd import lines
    
    logger.info("Today's input is {} lines".format(len(lines))) 
    part1(lines)
    part2(lines)