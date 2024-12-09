import time
from functools import wraps


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds.")
        return result

    return wrapper


def get_data():
    data = []
    file_id = 0
    with open("input.txt") as fin:
        line = fin.read().strip()
        for char_no, char in enumerate(line):
            if char_no % 2 == 0:  # block
                data.extend([file_id] * int(char))
                file_id += 1
            else:  # free
                data.extend([None] * int(char))
        return data


@timed
def part1():
    data = get_data()
    pointer = 0
    while True:
        if pointer == len(data):
            break
        if data[pointer] is None:
            while True:
                last_elem = data.pop()
                if last_elem is not None:
                    data[pointer] = last_elem
                    break
        pointer += 1
    checksum = 0
    for i, file_id in enumerate(data):
        checksum += file_id * i
    print("Part 1:",  checksum)


@timed
def part2():
    data = get_data()
    left_block_pointer = right_block_pointer = len(data) - 1
    while True:
        if left_block_pointer < 0:
            break
        # Find whole block
        if data[left_block_pointer] is None:
            left_block_pointer -= 1
            right_block_pointer = left_block_pointer
            continue
        while True:
            if left_block_pointer == 0 or data[left_block_pointer - 1] != data[right_block_pointer]:
                break
            left_block_pointer -= 1

        to_move = data[left_block_pointer]

        # Find first free window that fits
        left_free_pointer = right_free_pointer = 0
        found = False
        no_space_left = True
        while True:
            if right_free_pointer >= left_block_pointer:
                # Scanned through whole string and nothing found
                break
            if data[left_free_pointer] is not None:
                left_free_pointer += 1
                right_free_pointer += 1
                continue
            if right_free_pointer - left_free_pointer >= right_block_pointer - left_block_pointer:
                # Found window that fits
                found = True
                break
            right_free_pointer += 1
            no_space_left = False
            if data[right_free_pointer] is not None:
                right_free_pointer += 1
                left_free_pointer = right_free_pointer
                continue

        if not found:
            if no_space_left:
                break

            left_block_pointer -= 1
            right_block_pointer = left_block_pointer
            continue

        # File fits, perform move
        for i in range(left_free_pointer, right_free_pointer + 1):
            data[i] = to_move
        for i in range(left_block_pointer, right_block_pointer + 1):
            data[i] = None
        left_block_pointer -= 1
        right_block_pointer = left_block_pointer

    checksum = 0
    for i, file_id in enumerate(data):
        if file_id is None:
            continue
        checksum += file_id * i
    print("Part 2:",  checksum)


if __name__ == '__main__':
    part1()
    part2()