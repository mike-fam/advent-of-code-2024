from itertools import product


def get_data():
    data = {}
    zero_positions = []
    with open("input.txt") as fin:
        for line_no, line in enumerate(fin):
            line = line.strip()
            for char_no, char in enumerate(line):
                num = int(char)
                data[char_no, line_no] = num
                if num == 0:
                    zero_positions.append((char_no, line_no))
        size = char_no + 1, line_no + 1
        return data, zero_positions, size


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


def part1():
    data, zero_positions, size = get_data()
    score = 0
    for zero_position in zero_positions:
        # Depth-first search
        stack = [zero_position]
        visited = set()
        while len(stack) > 0:
            current_position = stack.pop()
            visited.add(current_position)
            if data[current_position] == 9:
                score += 1
                continue
            for neighbour in get_surrounding_positions(current_position, size):
                if data[neighbour] != data[current_position] + 1:
                    continue
                if neighbour in visited:
                    continue
                stack.append(neighbour)
    print(f"Part 1: {score}")


def part2():
    data, zero_positions, size = get_data()
    score = 0
    for zero_position in zero_positions:
        # Depth-first search WITHOUT visited
        stack = [zero_position]
        while len(stack) > 0:
            current_position = stack.pop()
            if data[current_position] == 9:
                score += 1
                continue
            for neighbour in get_surrounding_positions(current_position, size):
                if data[neighbour] != data[current_position] + 1:
                    continue
                stack.append(neighbour)
    print(f"Part 2: {score}")


if __name__ == "__main__":
    part1()
    part2()
