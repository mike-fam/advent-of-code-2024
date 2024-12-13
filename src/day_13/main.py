import math
import pprint
import time
from collections import deque, defaultdict
from functools import wraps
from itertools import product, chain
from typing import Optional


CoordinatePair = tuple[int, int]


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


def get_data():
    with open("input.txt") as fin:
        content = fin.read()
        raw_machines = content.split("\n\n")
        machines = []
        for raw_machine in raw_machines:
            btn_a = btn_b = prize = None
            for line in raw_machine.splitlines():
                if line.startswith("Button A: "):
                    ax = int(line[line.find("X+") + 2:line.find(",")])
                    ay = int(line[line.find("Y+") + 2:])
                    btn_a = (ax, ay)
                elif line.startswith("Button B: "):
                    bx = int(line[line.find("X+") + 2:line.find(",")])
                    by = int(line[line.find("Y+") + 2:])
                    btn_b = (bx, by)
                elif line.startswith("Prize: "):
                    px = int(line[line.find("X=") + 2:line.find(",")])
                    py = int(line[line.find("Y=") + 2:])
                    prize = (px, py)
            machines.append((btn_a, btn_b, prize))
        return machines


def is_prime(potential_prime: int):
    for i in range(2, math.ceil(potential_prime ** (1 / 2))):
        if potential_prime % i == 0:
            return False
    return True


def prime_factorization(n):
    prime_factors = {}
    n_copy = n
    for i in range(2, n_copy + 1):
        if not is_prime(i):
            continue
        exponent = 0
        while True:
            if n % i != 0:
                if exponent != 0:
                    prime_factors[i] = exponent
                break
            n = n // i
            exponent += 1
        if n == 1:
            break

    return prime_factors


def solve(machine):
    (a1, a2), (b1, b2), (c1, c2) = machine
    a1_factors = prime_factorization(a1)
    a2_factors = prime_factorization(a2)
    lcm_factors = {
        key: max(a1_factors.get(key, 0), a2_factors.get(key, 0))
        for key in set(a1_factors) | set(a2_factors)
    }
    lcm_a = 1
    for prime, exponent in lcm_factors.items():
        lcm_a *= prime ** exponent
    factor_1 = lcm_a // a1
    factor_2 = lcm_a // a2
    a1 *= factor_1
    b1 *= factor_1
    c1 *= factor_1
    a2 *= factor_2
    b2 *= factor_2
    c2 *= factor_2
    y = (c1 - c2) / (b1 - b2)
    x = (c1 - b1 * y) / a1
    return x, y


def get_cost(machines):
    cost = 0
    for machine in machines:
        x, y = solve(machine)
        if x != int(x) or y != int(y):
            # Unsolvable. x and y are expected to be whole numbers
            continue
        cost += x * 3 + y
    return cost


@timed
def part1():
    machines = get_data()
    cost = get_cost(machines)
    print(f"Part 1: {cost}")


@timed
def part2():
    machines = get_data()
    machines = [(*rest, (px + 10000000000000, py + 10000000000000)) for *rest, (px, py) in machines]
    cost = get_cost(machines)
    print(f"Part 2: {cost}")


if __name__ == "__main__":
    part1()
    part2()
