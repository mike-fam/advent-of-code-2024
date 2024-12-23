import time
from collections import defaultdict
from functools import wraps

CoordinatePair = tuple[int, int]
Position = Direction = CoordinatePair


DIRECTIONS = {
    (-1, 0),    # Left
    (1, 0),     # Right
    (0, -1),    # Up
    (0, 1),     # Down
}
WALL = "#"
FREE = "."
START = "S"
END = "E"


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
    walls = set()
    start = end = (0, 0)
    with open("input.txt") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            for char_no, char in enumerate(line):
                if char == WALL:
                    walls.add((char_no, line_no))
                elif char == START:
                    start = (char_no, line_no)
                elif char == END:
                    end = (char_no, line_no)
        return walls, start, end


def move(position: Position, direction: Direction):
    return position[0] + direction[0], position[1] + direction[1]


def get_manhattan_distance(p1: Position, p2: Position):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_jump_positions(position: Position, distances: dict[Position, int], manhattan_distance: int) -> set[Position]:
    surrounding_free_positions: set[Position] = set()
    for x in range(manhattan_distance + 1):
        for y in range(manhattan_distance + 1 - x):
            if x == y == 0:
                continue
            potential_positions = {
                move(position, (x, y)),
                move(position, (-x, y)),
                move(position, (x, -y)),
                move(position, (-x, -y)),
            }
            for potential_position in potential_positions:
                if potential_position in distances:
                    surrounding_free_positions.add(potential_position)
    return surrounding_free_positions


def get_potential_cheats(distances: dict[Position, int], cheat_length: int) -> set[tuple[Position, Position]]:
    potential_cheats: set[tuple[Position, Position]] = set()
    for position, distance in distances.items():
        free_jump_destinations = get_jump_positions(position, distances, cheat_length)

        if len(free_jump_destinations) <= 1:
            continue

        for free_jump_destination in free_jump_destinations:
            if free_jump_destination not in distances:
                continue
            if distances[free_jump_destination] < distance:
                continue
            potential_cheats.add((position, free_jump_destination))
    return potential_cheats


def get_distances(walls: set[Position], start: Position, end: Position) -> dict[Position, int]:
    current_distance = 0
    current_position = start
    distances = {}
    while True:
        distances[current_position] = current_distance
        if current_position == end:
            return distances
        for direction in DIRECTIONS:
            neighbour = move(current_position, direction)
            if neighbour in walls:
                continue
            if neighbour in distances:
                continue
            current_distance += 1
            current_position = neighbour
            break


def get_cheat_benefits(walls: set[Position], start: Position, end: Position, cheat_length: int) -> dict[int, set[tuple[Position, Position]]]:
    distances = get_distances(walls, start, end)
    potential_cheats = get_potential_cheats(distances, cheat_length)
    cheat_benefits: defaultdict[int, set[tuple[Position, Position]]] = defaultdict(set)

    for i, potential_cheat in enumerate(potential_cheats, start=1):
        print(f"\rEvaluating {potential_cheat}: {i}/{len(potential_cheats)}", end="")
        potential_cheat_start, potential_cheat_dest = potential_cheat
        saved_distance = distances[potential_cheat_dest] - distances[potential_cheat_start] - get_manhattan_distance(potential_cheat_start, potential_cheat_dest)

        cheat_benefits[saved_distance].add(potential_cheat)

    return cheat_benefits


@timed
def part1():
    walls, start, end = get_data()
    cheat_benefits = get_cheat_benefits(walls, start, end, 2)

    good_cheat_count = 0
    for benefit, cheats in cheat_benefits.items():
        if benefit >= 100:
            good_cheat_count += len(cheats)
    print(f"\nPart 1: {good_cheat_count}")


@timed
def part2():
    walls, start, end = get_data()
    cheat_benefits = get_cheat_benefits(walls, start, end, 20)

    good_cheat_count = 0
    for benefit, cheats in cheat_benefits.items():
        if benefit >= 100:
            good_cheat_count += len(cheats)
    print(f"\nPart 2: {good_cheat_count}")


if __name__ == '__main__':
    part1()
    part2()