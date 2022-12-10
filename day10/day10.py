from loguru import logger
from enum import Enum

class Inst(Enum):
    NOOP = "noop"
    ADDX = "addx"
    ADDX_OLD = "addx (2nd)"

class CRT:

    CRITICAL = [20, 60, 100, 140, 180, 220]

    def __init__(self):
        self.X = 1
        self.clk = 0
        self._inst = None
        self._arg = None
        self._critical_values = []
        self._output = ""

    def __str__(self):
        return f"@{self.clk}: X={self.X}  inst={self._inst} arg={self._arg}"

    def tick(self):
        self.clk += 1
        
        if self.clk in self.CRITICAL:
            self._critical_values.append( self.clk * self.X )

        if self._inst is Inst.NOOP:
            self._inst = None
            self._arg = None
        elif self._inst is Inst.ADDX:
            self._inst = Inst.ADDX_OLD
            self._arg = self._arg
        elif self._inst is Inst.ADDX_OLD:
            self._inst = None
            self.X = self.X + self._arg
            self._arg = None
        else:
            logger.debug("Invalid processor state! {}".format(self))

        if (self.clk % 40) in [self.X - 1, self.X, self.X + 1]:
            self._output += "█"
        else:
            self._output += " "
        if self.clk % 40 == 0:
            self._output += "\n"

        return self.clk
    
    def ready(self):
        return True if self._inst is None else False

    def issue(self, inst, arg):
        self._inst = inst
        self._arg = arg

def part1(data):
    crt = CRT()

    for line in data:
        toks = line.strip().split(" ")
        #logger.debug(" --> @{} {}".format(crt.clk, line.strip()))
        match toks[0]:
            case "noop":
                crt.issue(Inst.NOOP, None)
            case "addx":
                crt.issue(Inst.ADDX, int(toks[1]))
            case _:
                logger.debug("Unknown instruction {}".format(line.strip()))
        #logger.debug(crt)
        timer = crt.tick()
        
        while not crt.ready():
            timer = crt.tick()

    logger.debug(f"At end of program, X = {crt.X}")
    return(sum(crt._critical_values))

def part2(data):
    crt = CRT()

    for line in data:
        toks = line.strip().split(" ")
        #logger.debug(" --> @{} {}".format(crt.clk, line.strip()))
        match toks[0]:
            case "noop":
                crt.issue(Inst.NOOP, None)
            case "addx":
                crt.issue(Inst.ADDX, int(toks[1]))
            case _:
                logger.debug("Unknown instruction {}".format(line.strip()))
        #logger.debug(crt)
        timer = crt.tick()

        while not crt.ready():
            timer = crt.tick()

    while timer < 240:
        timer = crt.tick()

    print(crt._output)

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