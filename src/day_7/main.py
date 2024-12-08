import time
from enum import Enum
from functools import wraps
from typing import Callable
from math import ceil,log10


def timed(arg=None):
    def decorator(func):
        custom_name = arg if isinstance(arg, str) else None
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            function_name = custom_name or func.__name__
            print(f"Function '{function_name}' executed in {elapsed_time:.6f} seconds.")
            return result
        return wrapper
    if callable(arg):
        return decorator(arg)
    return decorator



class Operator(str, Enum):
    MULTIPLY = "*"
    ADD = "+"
    CONCAT = "||"


def get_data():
    data = {}
    with open("input.txt") as fin:
        for line in fin:
            line = line.strip()
            result, elements = line.split(": ")
            result = int(result)
            num_elements = list(map(int, elements.split(" ")))
            data[result] = num_elements
    return data


def mul(a: int, b: int):
    return a * b


def add(a: int, b: int):
    return a + b


def concat(a: int, b: int) -> int:
    return int(f"{a}{b}")


def rev_mul(res: int, a: int):
    return res // a


def rev_add(res: int, a: int):
    return res - a


def rev_concat(res: int, a: int):
    return int(str(res).removesuffix(str(a)))


def greater_than(res: int, b: int):
    return res >= b


def divisible(res: int, b: int):
    return res % b == 0


def is_suffix(res: int, b: int):
    return res != b and divisible(res - b, 10 ** ceil(log10(b)))


def get_sequence_values_brute(sequence: list[int], operators: list[Callable[[int, int], int]]) -> set[int]:
    if len(sequence) == 2:
        a, b = sequence
        return set(operator(a, b) for operator in operators)
    return set(operator(value, sequence[-1]) for operator in operators for value in get_sequence_values_brute(sequence[:-1], operators))


def validate_sequence_prune(result: int, sequence: list[int], reverse_operators: list[Callable[[int, int], int]], validators: list[Callable[[int, int], bool]]):
    if len(sequence) == 1:
        return sequence[0] == result

    for reverse_operator, validator in zip(reverse_operators, validators):
        if not validator(result, sequence[-1]):
            # Prune all paths that are known to be invalid
            continue
        if validate_sequence_prune(reverse_operator(result, sequence[-1]), sequence[:-1], reverse_operators, validators):
            return True
    return False


def solution_factory_brute(operators: list[Callable[[int, int], int]], name):
    @timed(f"{name} - Bruteforce")
    def solve():
        data = get_data()
        result_sum = 0
        for result, elements in data.items():
            if result in get_sequence_values_brute(elements, operators):
                result_sum += result
        print(f"{name}: {result_sum}")
        return result_sum
    return solve


def solution_factory_prune(reverse_operators: list[Callable[[int, int], int]], validators: list[Callable[[int, int], bool]], name):
    @timed(f"{name} - Prune")
    def solve():
        data = get_data()
        result_sum = 0
        for result, elements in data.items():
            if validate_sequence_prune(result, elements, reverse_operators, validators):
                result_sum += result
        print(f"{name}: {result_sum}")
        return result_sum
    return solve


part1_brute = solution_factory_brute([mul, add], "Part 1")
part2_brute = solution_factory_brute([mul, add, concat], "Part 2")
part1_prune = solution_factory_prune([rev_mul, rev_add], [divisible, greater_than], "Part 1")
part2_prune = solution_factory_prune([rev_mul, rev_add, rev_concat], [divisible, greater_than, is_suffix], "Part 2")


if __name__ == "__main__":
    # Both approaches are O(2^n) in worst case, but prune solution implements an AB-pruning-like functionality
    # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    part1_prune()  #  0.006251s
    part1_brute()  #  0.340681s
    part2_prune()  #  0.010736s
    part2_brute()  # 28.680787s
