import math
import pprint
import time
from collections import defaultdict
from functools import wraps

CoordinatePair = tuple[int, int]
Position = Direction = CoordinatePair


DIRECTIONS = {
    "<": (-1, 0),    # Left
    ">": (1, 0),     # Right
    "^": (0, -1),    # Up
    "v": (0, 1),     # Down
}


NUMERIC_CODE_POSITIONS = {
    "7": (0, 0), "8": (1, 0), "9": (2, 0),
    "4": (0, 1), "5": (1, 1), "6": (2, 1),
    "1": (0, 2), "2": (1, 2), "3": (2, 2),
                 "0": (1, 3), "A": (2, 3),
}

REVERSE_NUMERIC_CODE_POSITIONS = {position: key for key, position in NUMERIC_CODE_POSITIONS.items()}


DIRECTIONAL_CODE_POSITIONS = {
                 "^": (1, 0), "A": (2, 0),
    "<": (0, 1), "v": (1, 1), ">": (2, 1),
}

REVERSE_DIRECTIONAL_CODE_POSITIONS = {position: key for key, position in DIRECTIONAL_CODE_POSITIONS.items()}


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
        return fin.read().splitlines()


def move(position: Position, direction: Direction):
    return position[0] + direction[0], position[1] + direction[1]


def get_manhattan_distance(p1: Position, p2: Position):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def difference(p1: Position, p2: Position):
    return p1[0] - p2[0], p1[1] - p2[1]


def get_shortest_clicks(code: str, iteration: int, numeric: bool = False):
    if iteration == 0:
        return code
    code_position = NUMERIC_CODE_POSITIONS if numeric else DIRECTIONAL_CODE_POSITIONS
    last_position = code_position["A"]
    shortest_click_sequence = ""
    for char in code:
        current_position = code_position[char]
        last_pos_x, last_pos_y = last_position
        diff_x, diff_y = difference(current_position, last_position)
        up_down_char = "^" if diff_y < 0 else "v"
        left_right_char = "<" if diff_x < 0 else ">"
        hor_then_ver = left_right_char * abs(diff_x) + up_down_char * abs(diff_y) + "A"
        ver_then_hor = up_down_char * abs(diff_y)  + left_right_char * abs(diff_x) + "A"
        if (last_pos_x + diff_x, last_pos_y) not in code_position.values():
            shortest_click_sequence += get_shortest_clicks(ver_then_hor, iteration - 1)
        elif (last_pos_x, last_pos_y + diff_y) not in code_position.values():
            shortest_click_sequence += get_shortest_clicks(hor_then_ver, iteration - 1)
        else:
            shortest_click_sequence_ver_then_hor = get_shortest_clicks(ver_then_hor, iteration - 1)
            shortest_click_sequence_hor_then_ver = get_shortest_clicks(hor_then_ver, iteration - 1)
            if len(shortest_click_sequence_ver_then_hor) > len(shortest_click_sequence_hor_then_ver):
                shortest_click_sequence += shortest_click_sequence_hor_then_ver
            else:
                shortest_click_sequence += shortest_click_sequence_ver_then_hor
        last_position = current_position

    return shortest_click_sequence


def perform_clicks(code: str, iteration: int):
    if iteration == 0:
        return code
    code_position = DIRECTIONAL_CODE_POSITIONS
    reverse_position = REVERSE_DIRECTIONAL_CODE_POSITIONS
    if iteration == 1:
        code_position = NUMERIC_CODE_POSITIONS
        reverse_position = REVERSE_NUMERIC_CODE_POSITIONS
    current_position = code_position["A"]
    new_code = ""
    for char in code:
        if char == "A":
            new_code += reverse_position[current_position]
        else:
            current_position = move(current_position, DIRECTIONS[char])
            if current_position not in reverse_position:
                raise ValueError(f"Cannot find position {current_position} when trying to move {char}")
    return perform_clicks(new_code, iteration - 1)


@timed
def part1():
    codes = get_data()

    complexity = 0
    for code in codes:
        shortest_clicks = get_shortest_clicks(code, 3, numeric=True)
        complexity += int(code.removesuffix("A")) * len(shortest_clicks)
    print(f"Part 1: {complexity}")


@timed
def part2():
    codes = get_data()
    complexity = 0
    for code in codes:
        print(code)
        shortest_clicks = get_shortest_clicks(code, 25, numeric=True)
        complexity += int(code.removesuffix("A")) * len(shortest_clicks)
    print(f"Part 2: {complexity}")


if __name__ == '__main__':
    part1()
    # part2()