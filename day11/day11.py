from loguru import logger

import operator

class Monkey:

    def __init__(self, monkey_data):
        lines = monkey_data.split('\n')

        self._inspections = 0

        self._number = int(lines[0].split(' ')[1].rstrip(':'))

        toks = lines[1].split(':')[1].split(',')
        self._items = [int(x.strip()) for x in toks]
        
        op_toks = lines[2].split(':')[1].strip().split(' ')
        arg1 = op_toks[2]
        op = op_toks[3]
        arg2 = op_toks[4]

        func = None
        match op:
            case "*":
                func = operator.mul
            case "/":
                func = operator.truediv
            case "+":
                func = operator.add
            case "-":
                func = operator.sub
            case _:
                logger.error("Unknown operator in expression: {}", " ".join(op_toks))
                raise SyntaxError()

        if arg1 == "old" and arg2 != "old":
            self._operation = lambda x: func(x, int(arg2))
        elif arg1 != "old" and arg2 == "old":
            self._operation = lambda x: func(int(arg1), x)
        elif arg1 == "old" and arg2 == "old":
            self._operation = lambda x: func(x, x)
        else:
            self._operation = lambda x: func(int(arg1), int(arg2))

        # Test appears to always be a modulus check
        self._modulus = int(lines[3].split(' ')[-1])
        self._true_target = int(lines[4].split(' ')[-1])
        self._false_target = int(lines[5].split(' ')[-1])

    def take_turn(self, chill=False):
        #logger.debug("Monkey {} takes a turn!", self._number)
        throw_list = []
        for item in self._items:
            self._inspections += 1
            #logger.debug("  Monkey inspects item with a worry level of {}", item)
            post_inspection = self._operation(item)
            #logger.debug("    New worry level is {}", item)
            if not chill:
                new_worry = post_inspection // 3
            else:
                new_worry = post_inspection % self._common_mod
            #logger.debug("    Monkey gets bored - worry drops to {}", new_worry)
            if new_worry % self._modulus == 0:
                #logger.debug("    Mod Check is 0: throw to {}", self._true_target)
                throw_list.append([new_worry, self._true_target])
            else:
                #logger.debug("    Mod Check is not 0: throw to {}", self._false_target)
                throw_list.append([new_worry, self._false_target])
        self._items = []

        return throw_list

def parse_monkeys(data):
    chunky_monkeys = data.split("\n\n")
    logger.debug(len(chunky_monkeys))
    monkeys = {}
    for monkey_data in chunky_monkeys:
        monkey = Monkey(monkey_data)
        logger.debug(f"{monkey._number} --> {monkey._items}")
        monkeys[monkey._number] = monkey
    return monkeys

def part1(data):
    monkeys = parse_monkeys(data)

    for i in range(0, 20):
        for idx in sorted(monkeys.keys()):
            throw_list = monkeys[idx].take_turn()
            for item, target in throw_list:
                monkeys[target]._items.append(item)
            
    inspections = []
    for idx in sorted(monkeys.keys()):
        inspections.append(monkeys[idx]._inspections)
        
    monkey_business_level = sorted(inspections, reverse=True)
    return monkey_business_level[0] * monkey_business_level[1]

def part2(data):
    import functools
    import sys
    monkeys = parse_monkeys(data)

    moduli = [x._modulus for _, x in monkeys.items()]
    common_mod = functools.reduce(operator.mul, moduli)
    for _, x in monkeys.items():
        x._common_mod = common_mod

    for i in range(0, 10000):
        if i % 100 == 0:
            print('.', end='')
            sys.stdout.flush()
        for idx in sorted(monkeys.keys()):
            throw_list = monkeys[idx].take_turn(chill=True)
            for item, target in throw_list:
                monkeys[target]._items.append(item)
    print('')
            
    inspections = []
    for idx in sorted(monkeys.keys()):
        inspections.append(monkeys[idx]._inspections)
        
    monkey_business_level = sorted(inspections, reverse=True)
    return monkey_business_level[0] * monkey_business_level[1]
    

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            data = infile.read()
    else:
        #from aocd import lines
        from aocd import data
    
    logger.info("Today's input is {} lines".format(len(data))) 
    logger.info("Answer to part 1 is: {}".format(part1(data)))
    logger.info("Answer to part 2 is: {}".format(part2(data)))