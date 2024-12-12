import math
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
    data: dict[CoordinatePair, str] = {}
    with open("input.txt") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            for char_no, char in enumerate(line):
                data[char_no, line_no] = char
        size: CoordinatePair = char_no + 1, line_no + 1
        return data, size


def get_surrounding_positions(start_position, size):
    surrounding_positions = []
    start_x, start_y = start_position
    size_x, size_y = size
    for delta_x, delta_y in product((0, 1, -1), repeat=2):
        if delta_x == 0 and delta_y == 0:
            continue
        if delta_x != 0 and delta_y != 0:
            continue
        if not (0 <= start_x + delta_x < size_x):
            continue
        if not (0 <= start_y + delta_y < size_y):
            continue
        surrounding_positions.append((start_x + delta_x, start_y + delta_y))
    return surrounding_positions


def get_perimeter(region: set[CoordinatePair]):
    perimeter = 0
    for position in region:
        fence_count = 4
        for neighbour in get_surrounding_positions(position, (math.inf, math.inf)):
            if neighbour in region:
                fence_count -= 1
        perimeter += fence_count
    return perimeter


def find_regions(data: dict[CoordinatePair, str], size: CoordinatePair):
    visited = set()
    regions = []
    for position, char in data.items():
        current_region = set()
        if position in visited:
            continue
        # BFS
        queue = deque([position])
        while len(queue) > 0:
            current_position = queue.popleft()
            visited.add(current_position)
            current_region.add(current_position)
            for neighbour in get_surrounding_positions(current_position, size):
                if neighbour in visited:
                    continue
                if data[current_position] != data[neighbour]:
                    continue
                queue.appendleft(neighbour)
        regions.append(current_region)
    return regions


def get_edges(region: set[CoordinatePair]):
    horizontal_edges: defaultdict[int, set[CoordinatePair]] = defaultdict(set)
    vertical_edges: defaultdict[int, set[CoordinatePair]] = defaultdict(set)
    for position in region:
        pos_x, pos_y = position
        new_horizontal_edges = [position, (pos_x, pos_y + 1)]
        new_vertical_edges = [position, (pos_x + 1, pos_y)]
        for new_horizontal_edge in new_horizontal_edges:
            new_edge_x, new_edge_y = new_horizontal_edge
            new_edge = (new_edge_x, new_edge_x)
            if new_edge not in horizontal_edges[new_edge_y]:
                horizontal_edges[new_edge_y].add(new_edge)
            else:
                horizontal_edges[new_edge_y].remove(new_edge)
        for new_vertical_edge in new_vertical_edges:
            new_edge_x, new_edge_y = new_vertical_edge
            new_edge = (new_edge_y, new_edge_y)
            if new_edge not in vertical_edges[new_edge_x]:
                vertical_edges[new_edge_x].add(new_edge)
            else:
                vertical_edges[new_edge_x].remove(new_edge)
    for pivot, edges in enumerate((vertical_edges, horizontal_edges)):
        for edge_group, edges_of_group in edges.items():
            is_previous_cell_after_pivot: Optional[bool] = None
            previous_edge: Optional[CoordinatePair] = None
            joined_edges: set[CoordinatePair] = set()
            for edge in sorted(edges_of_group):
                edge_coord, *_ = edge
                if is_previous_cell_after_pivot is None:
                    is_previous_cell_after_pivot = ((edge_coord, edge_group) if pivot == 1 else (edge_group, edge_coord)) in region
                    previous_edge = edge
                    joined_edges.add(edge)
                    continue
                is_current_cell_after_pivot = ((edge_coord, edge_group) if pivot == 1 else (edge_group, edge_coord)) in region
                previous_edge_start, previous_edge_end = previous_edge
                current_edge_coord, *_ = edge
                if previous_edge_end == current_edge_coord - 1 and is_previous_cell_after_pivot == is_current_cell_after_pivot:
                    # Join edges
                    joined_edges.remove(previous_edge)
                    joined_edge = (previous_edge_start, current_edge_coord)
                    joined_edges.add(joined_edge)
                    previous_edge = joined_edge
                else:
                    joined_edges.add(edge)
                    previous_edge = edge
                is_previous_cell_after_pivot = is_current_cell_after_pivot
            edges[edge_group] = joined_edges
    return vertical_edges, horizontal_edges


@timed
def part1():
    data, size = get_data()
    regions = find_regions(data, size)
    fence_price = 0
    for region in regions:
        fence_price += len(region) * get_perimeter(region)
    print(f"Part 1: {fence_price}")


@timed
def part2():
    data, size = get_data()
    regions = find_regions(data, size)
    fence_price = 0
    for region in regions:
        horizontal_edges, vertical_edges = get_edges(region)
        fence_price += len(region) * (len(list(chain.from_iterable(horizontal_edges.values()))) +
                                      len(list(chain.from_iterable(vertical_edges.values()))))
    print(f"Part 2: {fence_price}")


if __name__ == "__main__":
    part1()
    part2()
