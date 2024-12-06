from collections import defaultdict
from itertools import chain
from pprint import pprint

# Left, up, right, down, clockwise
DIRECTIONS = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]

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



def part2():
    (size_x, size_y), start_position, obstacles = load_data()
    direction_index = 1  # Up
    new_obstacles = defaultdict(lambda: defaultdict(set))
    hit_obstacles = defaultdict(set)
    position = start_position
    while True:
        pos_x, pos_y = position
        if not (0 <= pos_x < size_x):
            break
        if not (0 <= pos_y < size_y):
            break
        
        # Scan for obstacles on the right
        direction = DIRECTIONS[direction_index]
        right_direction = DIRECTIONS[(direction_index + 1) % len(DIRECTIONS)]
        scan_pos = position
        while True:
            scan_pos = move(scan_pos, right_direction)
            scan_pos_x, scan_pos_y = scan_pos
            if not (0 <= scan_pos_x < size_x):
                break
            if not (0 <= scan_pos_y < size_y):
                break
            next_pos = move(position, direction)
            if scan_pos in obstacles and next_pos not in obstacles and next_pos != start_position:
                new_obstacles[right_direction][scan_pos].add(next_pos)
                break
                
        # Try to move, if not possible, then keep turning
        while True:
            direction = DIRECTIONS[direction_index]
            potential_move = move(position, direction)
            if potential_move in obstacles:
                direction_index = (direction_index + 1) % len(DIRECTIONS)
                hit_obstacles[direction].add(potential_move)
            else:
                position = potential_move
                break
    new_obstacle_positions = []
    for new_obstacles_at_direction in new_obstacles.values():
        for new_obstacle_positions_at_direction in new_obstacles_at_direction.values():
            new_obstacle_positions.extend(new_obstacle_positions_at_direction)
    print("Part 2:", len(new_obstacle_positions))


if __name__ == '__main__':
    part1()
    part2()