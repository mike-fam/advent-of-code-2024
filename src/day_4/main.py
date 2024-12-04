from enum import Enum
from itertools import product
from pprint import pprint


MOVEMENTS = set(product(range(-1, 2), repeat=2))
MOVEMENTS.remove((0, 0))
DIAGONAL_MOVEMENTS = set(movement for movement in MOVEMENTS if 0 not in movement)


def get_data():
    positions = {}
    with open("input.txt") as fin:
        for line_no, line in enumerate(fin):
            for char_no, char in enumerate(line.strip()):
               positions[char_no, line_no] = char
    return positions


def find_next_match(positions, pattern, movement, matches=None):
    total_matches = 0
    if len(pattern) == 0:
        return matches
    normalised_matches = matches
    new_matches = []
    if matches is None:
        move_x, move_y = movement
        normalised_matches = [[(pos_x - move_x, pos_y - move_y)] for pos_x, pos_y in positions]
    for existing_matches in normalised_matches:
        *_, last_match = existing_matches
        last_match_x, last_match_y = last_match
        move_x, move_y = movement
        new_pos = (last_match_x + move_x, last_match_y + move_y)
        new_pos_char = positions.get(new_pos)
        if new_pos_char != pattern[0]:
            continue
        new_match = [*existing_matches, new_pos] if matches is not None else [new_pos]
        new_matches.append(new_match)
    return find_next_match(positions, pattern[1:], movement, new_matches)
            


def part1():
    positions = get_data()
    matches = []
    for movement in MOVEMENTS:
        matches.extend(find_next_match(positions, "XMAS", movement))
    print("Part 1:", len(matches))
        

def part2():
    positions = get_data()
    matches = []
    found = set()
    found_twice = set()
    for movement in DIAGONAL_MOVEMENTS:
        matches.extend(find_next_match(positions, "MAS", movement))
    for _, middle_match, _ in matches:
        if middle_match in found:
            found_twice.add(middle_match)
        else:
            found.add(middle_match)
    print("Part 2:", len(found_twice))
                
        
if __name__ == "__main__":
    part1()
    part2()

