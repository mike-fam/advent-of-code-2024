from collections import defaultdict
from itertools import product, combinations

Position = tuple[int, int]

def get_data():
    data: defaultdict[str, set[Position]] = defaultdict(set)
    with open("input.txt") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            for char_no, char in enumerate(line):
                if char == ".":
                    continue
                data[char].add((char_no, line_no))
        size = char_no + 1, line_no + 1
        return data, size


def get_symmetric_position(side: Position, pivot: Position) -> Position:
    side_x, side_y = side
    pivot_x, pivot_y = pivot
    deta_x = pivot_x - side_x
    deta_y = pivot_y - side_y
    return side_x + 2 * deta_x, side_y + 2 * deta_y


def within_bound(position: Position, size: Position) -> bool:
    position_x, position_y = position
    size_x, size_y = size
    return 0 <= position_x < size_x and 0 <= position_y < size_y


def get_all_antinode_positions(antenna_pos_1: Position, antenna_pos_2: Position, size: Position) -> set[Position]:
    antinode_positions = {antenna_pos_1, antenna_pos_2}
    for pos_1, pos_2 in ((antenna_pos_1, antenna_pos_2), (antenna_pos_2, antenna_pos_1)):
        while True:
            new_antinode_pos = get_symmetric_position(pos_1, pos_2)
            if not within_bound(new_antinode_pos, size):
                break
            antinode_positions.add(new_antinode_pos)
            pos_1, pos_2 = pos_2, new_antinode_pos
    return antinode_positions


def part1():
    data, (size_x, size_y) = get_data()
    antinodes: set[Position] = set()
    for position in product(range(size_x), range(size_y)):

        for frequency, antennas in data.items():
            for antenna in antennas:
                if position == antenna:
                    continue
                if get_symmetric_position(position, antenna) in antennas:
                    antinodes.add(position)
                    break
            if position in antinodes:
                break
    print(f"Part 1: {len(antinodes)}")


def part2():
    data, size = get_data()
    antinodes: set[Position] = set()
    for frequency, antennas in data.items():
        for antenna_1, antenna_2 in combinations(antennas, r=2):
            antinodes.update(get_all_antinode_positions(antenna_1, antenna_2, size))
    print(f"Part 2: {len(antinodes)}")

if __name__ == '__main__':
    part1()
    part2()