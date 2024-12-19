import time
from functools import wraps


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
        content = fin.read().splitlines()
        available_patterns = content[0].split(", ")
        target_patterns = content[2:]
        return available_patterns, target_patterns


cache = {}
def possible_combinations_memo(available_patterns: list[str], target_pattern: str):
    # print(f"Evaluating {target_pattern} against {available_patterns}")
    if target_pattern in cache:
        return cache[target_pattern]
    combination_count = 0
    for available_pattern in available_patterns:
        if not target_pattern.startswith(available_pattern):
            continue
        if target_pattern == available_pattern:
            combination_count += 1
            continue
        combination_count += possible_combinations_memo(available_patterns, target_pattern.removeprefix(available_pattern))
    cache[target_pattern] = combination_count
    return combination_count


def possible_combinations_bottom_up(available_patterns: list[str], target_pattern: str):
    pattern_length = len(target_pattern)
    # pattern_construction_count[i] represents the number of ways to construct target_pattern[:i]
    pattern_construction_count = [0] * (pattern_length + 1)
    pattern_construction_count[0] = 1  # Base case: 1 way to construct an empty target pattern

    for i in range(1, pattern_length + 1):
        for pattern in available_patterns:
            if i >= len(pattern) and target_pattern[i - len(pattern):i] == pattern:
                pattern_construction_count[i] += pattern_construction_count[i - len(pattern)]

    return pattern_construction_count[pattern_length]


@timed
def part1():
    available_patterns, target_patterns = get_data()
    possible_patterns = []
    for target_pattern in target_patterns:
        if possible_combinations_memo(available_patterns, target_pattern) > 0:
        # if possible_combinations_bottom_up(available_patterns, target_pattern) > 0:
            possible_patterns.append(target_pattern)
    print(f"Part 1: {len(possible_patterns)}")


@timed
def part2():
    available_patterns, target_patterns = get_data()
    possible_patterns = 0
    for target_pattern in target_patterns:
        possible_patterns += possible_combinations_bottom_up(available_patterns, target_pattern)
        # possible_patterns += possible_combinations_memo(available_patterns, target_pattern)
    print(f"Part 2: {possible_patterns}")


if __name__ == '__main__':
    part1()
    part2()