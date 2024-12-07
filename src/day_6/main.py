import time
from collections import defaultdict
from functools import wraps
from itertools import product

# Left, up, right, down, clockwise
DIRECTIONS = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds.")
        return result

    return wrapper


def load_data():
    obstacles = set()
    initial_position = ()
    with open("input.txt") as fin:
        for line_no, line in enumerate(fin.readlines()):
            for char_no, char in enumerate(line):
                if char == "#":
                    obstacles.add((char_no, line_no))
                elif char == "^":
                    initial_position = (char_no, line_no)
        size = (char_no + 1, line_no + 1)
        return size, initial_position, obstacles


def move(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


@timed
def part1():
    (size_x, size_y), position, obstacles = load_data()
    positions_passed = set()
    direction_index = 1  # Up
    while True:
        pos_x, pos_y = position
        if not (0 <= pos_x < size_x):
            break
        if not (0 <= pos_y < size_y):
            break
        # Try to move, if not possible, then keep turning
        positions_passed.add(position)
        while True:
            potential_move = move(position, DIRECTIONS[direction_index])
            if potential_move in obstacles:
                direction_index = (direction_index + 1) % len(DIRECTIONS)
            else:
                position = potential_move
                break
    print("Part 1:", len(positions_passed))


@timed
def part2():
    (size_x, size_y), start_position, obstacles = load_data()
    new_obstacles = set()
    potential_new_obstacles = product(range(size_x), range(size_y))
    for potential_obstacle in potential_new_obstacles:
        if potential_obstacle in obstacles or potential_obstacle == start_position:
            continue
        direction_index = 1  # Up
        position = start_position
        test_obstacles = obstacles.copy()
        test_obstacles.add(potential_obstacle)
        passed_positions = defaultdict(set)
        while True:
            pos_x, pos_y = position
            if not (0 <= pos_x < size_x):
                break
            if not (0 <= pos_y < size_y):
                break
            if direction_index in passed_positions[position]:
                # Now in a loop
                new_obstacles.add(potential_obstacle)
                break
            passed_positions[position].add(direction_index)
            # Try to move, if not possible, then keep turning
            while True:
                direction = DIRECTIONS[direction_index]
                potential_move = move(position, direction)
                if potential_move in test_obstacles:
                    direction_index = (direction_index + 1) % len(DIRECTIONS)
                else:
                    position = potential_move
                    break
    print("Part 2:", len(new_obstacles))


if __name__ == '__main__':
    part1()
    part2()