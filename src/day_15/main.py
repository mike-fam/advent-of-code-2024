import time
from collections import defaultdict
from functools import wraps, reduce

CoordinatePair = tuple[int, int]


WALL = "#"
FREE = "."
BOX = "O"
DOUBLE_BOX_FIRST = "["
DOUBLE_BOX_LAST = "]"
ROBOT = "@"
DOUBLE_BOX = DOUBLE_BOX_FIRST + DOUBLE_BOX_LAST


DIRECTIONS = {
    "<": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
}


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


def get_data(raw: str):
    data = defaultdict(set)
    moves = []
    raw_map, raw_moves = raw.split("\n\n")
    for line_no, map_line in enumerate(raw_map.splitlines()):
        for char_no, char in enumerate(map_line):
            if char == FREE:
                continue
            data[char].add((char_no, line_no))
    raw_moves = "".join(raw_moves.splitlines())
    for raw_move in raw_moves:
        moves.append(DIRECTIONS[raw_move])

    return data, moves


def get_data_part_1():
    with open("input.txt") as fin:
        raw = fin.read()
        return get_data(raw)


def get_data_part_2():
    with open("input.txt") as fin:
        raw = fin.read()
        raw = raw.replace(WALL, WALL * 2)
        raw = raw.replace(BOX, DOUBLE_BOX_FIRST + DOUBLE_BOX_LAST)
        raw = raw.replace(FREE, FREE * 2)
        raw = raw.replace(ROBOT, ROBOT + FREE)
        return get_data(raw)


def move(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


def make_move_part_1(data: dict[str, set], direction: CoordinatePair):
    data_copy = data.copy()
    from_ = data_copy[ROBOT].pop()
    first_move = last_move = move(from_, direction)
    while True:
        if last_move in data[WALL]:
            # Don't make any move if WALL is hit
            data_copy[ROBOT].add(from_)
            return data_copy
        if last_move not in data[BOX]:
            data_copy[BOX].add(last_move)
            break
        # last_move hits a BOX, check next box
        last_move = move(last_move, direction)
    data_copy[BOX].remove(first_move)
    data_copy[ROBOT].add(first_move)
    return data_copy


def make_move_part_2(data: dict[str, set], direction: CoordinatePair):
    data_copy = data.copy()
    from_ = data_copy[ROBOT].pop()
    first_move = move(from_, direction)
    last_affected_squares = {first_move}
    found_double_box_last_positions = set()
    found_double_box_first_positions = set()
    while True:
        if len(last_affected_squares.intersection(data[WALL])) > 0:
            # Don't make any move if WALL is hit
            data_copy[ROBOT].add(from_)
            return data_copy
        intercept_with_double_box_first_positions = last_affected_squares.intersection(data[DOUBLE_BOX_FIRST])
        intercept_with_double_box_last_positions = last_affected_squares.intersection(data[DOUBLE_BOX_LAST])

        # All affected squares free
        if len(intercept_with_double_box_first_positions) == 0 and len(intercept_with_double_box_last_positions) == 0:
            for found_box_positions, box_key in zip((found_double_box_first_positions, found_double_box_last_positions), DOUBLE_BOX):
                data_copy[box_key] -= found_box_positions
                data_copy[box_key].update(move(found_box_position, direction)
                                          for found_box_position in found_box_positions)
            break

        # handle box cells
        for box_first_position in intercept_with_double_box_first_positions:
            intercept_with_double_box_last_positions.add((box_first_position[0] + 1, box_first_position[1]))
        for box_last_position in intercept_with_double_box_last_positions:
            intercept_with_double_box_first_positions.add((box_last_position[0] - 1, box_last_position[1]))
        all_intercept_positions = intercept_with_double_box_first_positions | intercept_with_double_box_last_positions
        found_double_box_first_positions.update(intercept_with_double_box_first_positions)
        found_double_box_last_positions.update(intercept_with_double_box_last_positions)
        last_affected_squares.clear()
        for affected_position in all_intercept_positions:
            new_affected_position = move(affected_position, direction)
            if new_affected_position not in all_intercept_positions:
                last_affected_squares.add(new_affected_position)

    data_copy[ROBOT].add(first_move)
    return data_copy


# Helper for debugging
def print_map(data: dict[str, set[CoordinatePair]]):
    inverted_data = {}
    size_x = size_y = 0
    for char, positions in data.items():
        for pos_x, pos_y in positions:
            if pos_x >= size_x:
                size_x = pos_x
            if pos_y >= size_y:
                size_y = pos_y
            inverted_data[pos_x, pos_y] = char
    size_x += 1
    size_y += 1
    for y in range(size_y):
        for x in range(size_x):
            if (x - 1, y) in data[DOUBLE_BOX]:
                continue
            if (x, y) in inverted_data:
                print(inverted_data[(x, y)], end="")
            else:
                print(FREE, end="")
        print()


@timed
def part1():
    data, moves = get_data_part_1()
    for direction in moves:
        data = make_move_part_1(data, direction)
    gps_sum = 0
    for box_x, box_y in data[BOX]:
        gps_sum += box_x + box_y * 100
    print(f"Part 1: {gps_sum}")


@timed
def part2():
    data, moves = get_data_part_2()
    for direction in moves:
        data = make_move_part_2(data, direction)
    gps_sum = 0
    for box_x, box_y in data[DOUBLE_BOX_FIRST]:
        gps_sum += box_x + box_y * 100
    print(f"Part 2: {gps_sum}")


if __name__ == "__main__":
    part1()
    part2()
