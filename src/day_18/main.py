import math
import time
from collections import defaultdict, deque
from functools import wraps
from typing import TypeVar, Generic, Optional


CoordinatePair = tuple[float, float]
Position = Direction = CoordinatePair
T = TypeVar("T")


DIRECTIONS = {
    (-1, 0),    # Left
    (1, 0),     # Right
    (0, -1),    # Up
    (0, 1),     # Down
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


def get_data(filename: str):
    walls: list[Position] = []
    size = 70 if filename == "input.txt" else 6
    with open(filename) as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            first, second = line.split(",")
            walls.append((int(first), int(second)))
        return walls, size


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

    def __repr__(self):
        return f"Queue({self._sequence})"


def dijkstra(walls: list[Position], start: Position, end: Position, size: int) \
        -> dict[Direction, float]:
    distances: dict[Position, float] = defaultdict(lambda: math.inf)
    queue: PriorityQueue[Position] = PriorityQueue()
    queue.push(start, 0)
    visited: set[Position] = set()
    distances[start] = 0

    while len(queue) > 0:
        priority, current_position = queue.pop()
        visited.add(current_position)
        if current_position == end:
            # Found end
            break
        for direction in DIRECTIONS:
            neighbour = move(current_position, direction)
            neighbour_x, neighbour_y = neighbour
            if neighbour in visited:
                continue
            if neighbour_x > size or neighbour_y > size:
                continue
            if neighbour_x < 0 or neighbour_y < 0:
                continue
            if neighbour in walls:
                continue
            neighbour_existing_distance = distances[neighbour]
            neighbour_new_distance = priority + 1
            if neighbour_new_distance <= neighbour_existing_distance:
                queue.update_priority(neighbour, neighbour_new_distance)
                distances[neighbour] = neighbour_new_distance
    return distances


@timed
def part1():
    walls, size = get_data("input.txt")
    start = 0, 0
    end = size, size
    distances = dijkstra(walls[:1024], start, end, size)
    print(f"Part 1: {distances[end]}")


@timed
def part2():
    walls, size = get_data("input.txt")
    start = 0, 0
    end = size, size

    # Binary search
    min_i = 1024
    max_i = len(walls)
    while True:
        if min_i == max_i - 1:
            break
        test_i = (min_i + max_i) // 2
        distances = dijkstra(walls[:test_i], start, end, size)
        if distances[end] == math.inf:
            print(test_i, "too high")
            max_i = test_i
        else:
            print(test_i, "too low")
            min_i = test_i
    print(f"Part 2: {walls[min_i]}")


if __name__ == "__main__":
    part1()
    part2()
