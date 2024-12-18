import math
import pprint
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import wraps
from typing import TypeVar, Generic, Optional


def timed(arg=None):
    def decorator(func):
        custom_name = arg if isinstance(arg, str) else None
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time_time = time.perf_counter()
            elapsed_time = end_time_time - start_time_time
            function_name = custom_name or func.__name__
            print(f"Function '{function_name}' executed in {elapsed_time:.6f} seconds.")
            return result
        return wrapper
    if callable(arg):
        return decorator(arg)
    return decorator


@dataclass
class Computer:
    register_a: int = 0
    register_b: int = 0
    register_c: int = 0
    pointer: int = 0
    skip_pointer_move: bool = False
    program: list[int] = field(default_factory=list)

    def __post_init__(self):
        self.output = []

    def combo_operand(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.register_a
        elif operand == 5:
            return self.register_b
        elif operand == 6:
            return self.register_c
        else:
            raise ValueError(f"Invalid operand '{operand}'")

    def _adv(self, operand: int):
        # print(f"adv({operand})")
        self.register_a //= 2 ** self.combo_operand(operand)

    def _bxl(self, operand: int):
        # print(f"bxl({operand})")
        self.register_b ^= operand

    def _bst(self, operand: int):
        # print(f"bst({operand})")
        self.register_b = self.combo_operand(operand) % 8

    def _jnz(self, operand: int):
        # print(f"jnz({operand})")
        if self.register_a == 0:
            return
        self.pointer = self.combo_operand(operand)
        self.skip_pointer_move = True

    def _bxc(self, operand: int):
        # print(f"bxc({operand})")
        self.register_b ^= self.register_c

    def _out(self, operand: int):
        # print(f"out({operand})")
        output = self.combo_operand(operand) % 8
        self.output.append(output)

    def _bdv(self, operand: int):
        # print(f"bdv({operand})")
        self.register_b = self.register_a // 2 ** self.combo_operand(operand)

    def _cdv(self, operand: int):
        # print(f"cdv({operand})")
        self.register_c = self.register_a // 2 ** self.combo_operand(operand)

    def run_operation(self, opcode: int, operand: int):
        if opcode == 0:
            return self._adv(operand)
        elif opcode == 1:
            return self._bxl(operand)
        elif opcode == 2:
            return self._bst(operand)
        elif opcode == 3:
            return self._jnz(operand)
        elif opcode == 4:
            return self._bxc(operand)
        elif opcode == 5:
            return self._out(operand)
        elif opcode == 6:
            return self._bdv(operand)
        elif opcode == 7:
            return self._cdv(operand)

    @classmethod
    def load(cls, filename: str):
        instance = cls()
        with open(filename) as fin:
            for line in fin:
                line = line.strip()
                if line.startswith("Register A:"):
                    instance.register_a = int(line.strip().removeprefix("Register A: "))
                elif line.startswith("Register B:"):
                    instance.register_b = int(line.strip().removeprefix("Register B: "))
                elif line.startswith("Register C:"):
                    instance.register_c = int(line.strip().removeprefix("Register C: "))
                elif line.startswith("Program: "):
                    instance.program = [int(num) for num in line.removeprefix("Program: ").split(",")]
        return instance

    def copy(self):
        copy = Computer()
        copy.register_a = self.register_a
        copy.register_b = self.register_b
        copy.register_c = self.register_c
        copy.pointer = self.pointer
        copy.skip_pointer_move = self.skip_pointer_move
        copy.program = self.program
        return copy

    def run(self, print_output=True):
        while self.pointer < len(self.program):
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            self.run_operation(opcode, operand)
            if not self.skip_pointer_move:
                self.pointer += 2
            self.skip_pointer_move = False
        if print_output:
            print(",".join(str(output) for output in self.output))

    def test_reg_a(self):
        valid_reg_a = []
        stack = [i for i in range(8)]
        while len(stack) > 0:
            test_reg_a = stack.pop()
            copy = self.copy()
            copy.register_a = test_reg_a
            copy.run(print_output=False)
            if all(output == self.program[-i] for i, output in enumerate(reversed(copy.output), start=1)):
                if len(copy.output) == len(self.program):
                    print(f"Found valid register a: {test_reg_a}")
                    valid_reg_a.append(test_reg_a)
                else:
                    print(f"Found register '{test_reg_a}' with valid output tail {copy.output}")
                    for next_test_reg_a in range(test_reg_a * 8, (test_reg_a + 1) * 8):
                        stack.append(next_test_reg_a)
        if len(valid_reg_a) == 0:
            print("Cannot find a suitable register a value")
        else:
            print(f"Minimum register a value: {min(valid_reg_a)}")


@timed
def part1():
    computer = Computer().load("input.txt")
    computer.run()


@timed
def part2():
    computer = Computer().load("input.txt")
    computer.test_reg_a()


if __name__ == "__main__":
    part1()
    part2()
