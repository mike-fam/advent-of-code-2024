import math
import time
from collections import defaultdict
from functools import wraps
from typing import TypeVar, Generic, Optional


CoordinatePair = tuple[float, float]
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
    walls: set[CoordinatePair] = set()
    start: Optional[CoordinatePair] = None
    end: Optional[CoordinatePair] = None
    with open("input_small.txt") as fin:
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


def move(position: CoordinatePair, direction: CoordinatePair):
    return position[0] + direction[0], position[1] + direction[1]


def position_delta(position_1: CoordinatePair, position_2: CoordinatePair):
    return position_1[0] - position_2[0], position_1[1] - position_2[1]


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


def dijkstra(walls: set[CoordinatePair], start: CoordinatePair, end: CoordinatePair) \
        -> tuple[Optional[dict[CoordinatePair, float]],
                 Optional[dict[CoordinatePair, Optional[CoordinatePair]]]]:
    distances: dict[CoordinatePair, float] = {}
    previous: dict[CoordinatePair, Optional[CoordinatePair]] = {}
    previous_directions: dict[CoordinatePair, CoordinatePair] = {}
    queue: PriorityQueue[CoordinatePair] = PriorityQueue()
    queue.push(start, 0)
    distances[start] = 0
    previous[start] = None
    previous_directions[start] = (1, 0)  # First facing east

    while len(queue) > 0:
        priority, current_position = queue.pop()
        if current_position == end:
            # Found end
            return distances, previous
        for direction in DIRECTIONS:
            neighbour = move(current_position, direction)
            if neighbour in walls:
                continue
            previous_direction = previous_directions[current_position]
            neighbour_priority = queue.get_priority(neighbour)
            new_neighbour_priority = priority + (1 if direction == previous_direction else 1001)
            if new_neighbour_priority < neighbour_priority:
                queue.push(neighbour, new_neighbour_priority)
                previous_directions[neighbour] = direction
                distances[neighbour] = new_neighbour_priority
                previous[neighbour] = current_position

    # Haven't found end
    return None, None


@timed
def part1():
    walls, start, end = get_data()
    distances, _ = dijkstra(walls, start, end)
    print(f"Part 1: {distances[end]}")


