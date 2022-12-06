import copy
import re
from abc import ABC, abstractmethod

with open("input.txt") as f:
    input = f.readlines()


def find_key_index():
    i = 0
    for line in input:
        if len(line) == 1 and line.isspace():
            return i - 1
        i += 1
    return -1


# abuse the fact that (at least for my test input), there are no multi-digit column keys
# thus, we only really need to find the char positions of each of the numerical keys, and
# since the crate's markers are also all single chars, we can just grab everything at those character positions.
# no need to parse brackets or anything.
key_index = find_key_index()


def build_stacks(input, key_index):
    stack_positions = {}

    for idx, c in enumerate(input[key_index]):
        if c.isspace():
            continue
        else:
            stack_positions[idx] = int(c)

    stacks = {stack_positions[k]: [] for k in stack_positions}

    for i in range(key_index - 1, -1, -1):
        line = input[i]
        for pos in stack_positions:
            if not line[pos].isspace():
                stack = stack_positions[pos]
                stacks[stack].append(line[pos])

    return stacks


stacks = build_stacks(input, key_index)


class Solver(ABC):

    _MOVEMENT_PROCEDURE_REGEX = re.compile(r"move (\d+) from (\d+) to (\d+)")

    move_instructions = None

    def __init__(self, stacks):
        self._stacks = copy.deepcopy(stacks)

    def parse_movement_procedure(self, line):
        movement_procedure = self._MOVEMENT_PROCEDURE_REGEX.findall(line)[0]

        move_count = int(movement_procedure[0])
        move_source = int(movement_procedure[1])
        move_target = int(movement_procedure[2])

        return (move_count, move_source, move_target)

    def solve(self):
        for move in self.move_instructions:
            move_count, move_source, move_target = self.parse_movement_procedure(move)
            source_stack = self._stacks[move_source]
            target_stack = self._stacks[move_target]

            self.consume_move_instructions(move_count,
                                           source_stack,
                                           target_stack)

    def print_result(self):
        results = []
        for k in self._stacks:
            stack = self._stacks[k]
            results.append(stack[len(stack)-1])

        print("".join(results))

    @abstractmethod
    def consume_move_instructions(self, move_count, source_stack, target_stack):
        pass


class Part1Solver(Solver):
    def consume_move_instructions(self, move_count, source_stack, target_stack):
        for _ in range(move_count):
            target_stack.append(source_stack.pop())


class Part2Solver(Solver):
    def consume_move_instructions(self, move_count, source_stack, target_stack):
        move_block = source_stack[-move_count:]
        target_stack.extend(move_block)

        del source_stack[-move_count:]


# skip the key and blank line after
Solver.move_instructions = input[key_index + 2:]

solver = Part1Solver(stacks)
solver.solve()
solver.print_result()

solver = Part2Solver(stacks)
solver.solve()
solver.print_result()
