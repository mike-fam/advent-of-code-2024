import math
import pprint
import time
from collections import defaultdict, deque
from functools import wraps
from typing import TypeVar, Generic, Optional


CoordinatePair = tuple[float, float]
Position = Direction = CoordinatePair
T = TypeVar("T")


WALL = "#"
START = "S"
END = "E"


DIRECTIONS = {
    (-1, 0),    # Left
    (1, 0),     # Right
    (0, -1),    # Up
    (0, 1),     # Down
}

DIRECTIONS_REPR = {
    (-1, 0): "<",
    (1, 0): ">",
    (0, -1): "^",
    (0, 1): "v",
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


def get_data():
    walls: set[Position] = set()
    start: Optional[Position] = None
    end: Optional[Position] = None
    with open("input.txt") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            for char_no, char in enumerate(line):
                if char == WALL:
                    walls.add((char_no, line_no))
                if char == START:
                    start = (char_no, line_no)
                elif char == END:
                    end = (char_no, line_no)
        return walls, start, end


def move(position: Position, direction: Direction):
    return position[0] + direction[0], position[1] + direction[1]


def position_delta(position_1: Position, position_2: Position):
    return position_1[0] - position_2[0], position_1[1] - position_2[1]


def invert(direction: Direction):
    return -direction[0], -direction[1]


class PriorityQueue(Generic[T]):
    def __init__(self):
        self._sequence: list[tuple[float, T]] = []
        self._item_to_priority: defaultdict[T, float] = defaultdict(lambda: math.inf)

    def push(self, item: T, priority: float):
        self._sequence.append((priority, item))
        self._item_to_priority[item] = priority
        self._sequence.sort(key=lambda entry: -entry[0])

    def pop(self):
        return self._sequence.pop()

    def update_priority(self, item: T, priority: float):
        for i, (_, existing_item) in enumerate(self._sequence):
            if existing_item == item:
                self._sequence.pop(i)
                break
        self.push(item, priority)
        self._item_to_priority[item] = priority

    def get_priority(self, item: T):
        return self._item_to_priority[item]

    def __len__(self):
        return len(self._sequence)


def print_map(walls, visited, start, end):
    size_y = start[1] + 2
    size_x = end[0] + 2
    for y in range(size_y):
        for x in range(size_x):
            if (x, y) == start:
                print(START, end="")
            elif (x, y) == end:
                print(END, end="")
            elif (x, y) in visited:
                print(DIRECTIONS_REPR[visited[(x, y)]], end="")
            elif (x, y) in walls:
                print(WALL, end="")
            else:
                print(" ", end="")
        print()


def dijkstra(walls: set[Position], start: Position, end: Position) \
        -> Optional[dict[Position, dict[Direction, float]]]:
    distances: dict[Position, dict[Direction, float]] = defaultdict(lambda: defaultdict(lambda: math.inf))
    queue: PriorityQueue[tuple[Position, Direction]] = PriorityQueue()
    queue.push((start, (1, 0)), 0)
    distances[start][(1, 0)] = 0

    while len(queue) > 0:
        priority, (current_position, last_direction) = queue.pop()
        if current_position == end:
            # Found end
            break
        for direction in DIRECTIONS:
            if direction == invert(last_direction):
                continue
            neighbour = move(current_position, direction)
            if neighbour in walls:
                continue
            neighbour_existing_distance = distances[neighbour][direction]
            neighbour_new_distance = priority + (1 if direction == last_direction else 1001)
            if neighbour_new_distance <= neighbour_existing_distance:
                queue.push((neighbour, direction), neighbour_new_distance)
                distances[neighbour][direction] = neighbour_new_distance
    return distances


@timed
def part1():
    walls, start, end = get_data()
    distances = dijkstra(walls, start, end)
    print(f"Part 1: {min(distances[end].values())}")


def extract_best_paths(distances: dict[Position, dict[Direction, float]], start: CoordinatePair, end: CoordinatePair):
    best_paths: dict[Position, set[Position]] = { }
    queue: deque[tuple[Position, Direction, float]] = deque()
    min_end_distance = min(distances[end].values())
    for direction_from_preceding_node, distance in distances[end].items():
        if distance > min_end_distance:
            continue
        preceding_node = move(end, invert(direction_from_preceding_node))
        queue.append((preceding_node, direction_from_preceding_node, min_end_distance))
        best_paths[preceding_node] = { end }
    while len(queue) > 0:
        current_node, direction_to_following_node, previous_distance = queue.popleft()
        if current_node == start:
            return best_paths
        for direction_from_preceding_node, distance in distances[current_node].items():
            if (direction_from_preceding_node == direction_to_following_node and distance + 1 == previous_distance) or \
                    (direction_from_preceding_node != direction_to_following_node and distance + 1001 == previous_distance):
                preceding_node = move(current_node, invert(direction_from_preceding_node))
                queue.append((preceding_node, direction_from_preceding_node, distance))
                if preceding_node not in best_paths:
                    best_paths[preceding_node] = set()
                best_paths[preceding_node].add(current_node)
    raise ValueError("Cannot find path from start to end.")


@timed
def part2():
    walls, start, end = get_data()
    distances = dijkstra(walls, start, end)
    best_paths = extract_best_paths(distances, start, end)
    best_path_squares = set()
    queue = deque([start])
    while len(queue) > 0:
        current_node = queue.popleft()
        best_path_squares.add(current_node)
        if current_node not in best_paths:
            continue
        for successor in best_paths[current_node]:
            queue.appendleft(successor)
    print(f"Part 2: {len(best_path_squares)}")


if __name__ == "__main__":
    part1()
    part2()
