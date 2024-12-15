import math
import sys
import time
from collections import defaultdict
from functools import wraps
from itertools import count

CoordinatePair = tuple[int, int]


SIZE = 101, 103


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
    robots = []
    with open("input.txt") as fin:
        for line in fin:
            line = line.strip()
            raw_position, raw_velocity = line.split()
            raw_position = raw_position.removeprefix("p=")
            raw_velocity = raw_velocity.removeprefix("v=")
            pos: CoordinatePair = tuple(map(int, raw_position.split(",")))
            vel: CoordinatePair = tuple(map(int, raw_velocity.split(",")))
            robots.append((pos, vel))
    return robots


def move(position, velocity, size, repeat):
    pos_x, pos_y = position
    vel_x, vel_y = velocity
    size_x, size_y = size
    new_pos_x = (pos_x + vel_x * repeat) % size_x
    new_pos_y = (pos_y + vel_y * repeat) % size_y
    return new_pos_x, new_pos_y


@timed
def part1():
    robots = get_data()
    quadrants = [[] for _ in range(4)]
    size_x, size_y = SIZE
    half_size_x, half_size_y = size_x // 2, size_y // 2
    for position, velocity in robots:
        new_position = move(position, velocity, SIZE, 100)
        new_pos_x, new_pos_y = new_position
        if new_pos_x < half_size_x and new_pos_y < half_size_y:
            quadrants[0].append(new_position)
        elif new_pos_x > half_size_x and new_pos_y < half_size_y:
            quadrants[1].append(new_position)
        elif new_pos_x < half_size_x and new_pos_y > half_size_y:
            quadrants[2].append(new_position)
        elif new_pos_x > half_size_x and new_pos_y > half_size_y:
            quadrants[3].append(new_position)

    safety_factor = 1
    for quadrant in quadrants:
        safety_factor *= len(quadrant)
    print(f"Part 1: {safety_factor}")


def part2():
    robots = get_data()
    min_deviation = math.inf
    size_x, size_y = SIZE

    for i in count(start=1):
        all_positions = defaultdict(int)
        for position, velocity in robots:
            all_positions[move(position, velocity, SIZE, i)] += 1
        mean_position_x = sum(position_x for position_x, _ in all_positions) / len(robots)
        mean_position_y = sum(position_y for _, position_y in all_positions) / len(robots)
        deviation_x = deviation_y = 0
        for (position_x, position_y), occurrences in all_positions.items():
            deviation_x += (position_x - mean_position_x) ** 2 * occurrences
            deviation_y += (position_y - mean_position_y) ** 2 * occurrences
        deviation = deviation_x / len(all_positions) + deviation_y / len(all_positions)
        if deviation > min_deviation:
            continue
        for y in range(size_y):
            for x in range(size_x):
                occurrence = all_positions[x, y]
                if occurrence == 0:
                    print(".", end="")
                else:
                    print(occurrence, end="")
            print()
        if input(f"Second {i} - Min deviation {min_deviation} - Does this look like a Christmas tree (y/N)? ") == "y":
            break

        min_deviation = deviation

    print(f"Part 2: {i}")


if __name__ == "__main__":
    part1()
    part2()
