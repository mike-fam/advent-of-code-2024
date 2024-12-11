import threading
import time
from collections import defaultdict
from functools import wraps


def timed(arg=None):
    def decorator(func):
        custom_name = arg if isinstance(arg, str) else None
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            function_name = custom_name or func.__name__
            print(f"Function '{function_name}' executed in {elapsed_time:.6f} seconds.")
            return result
        return wrapper
    if callable(arg):
        return decorator(arg)
    return decorator


def get_data():
    with open("input.txt") as fin:
        content = fin.read().strip().split()
        return list(map(int, content))


def blink(sequence: list[int], steps=1):
    if steps == 0:
        return sequence
    new_sequence = []
    for i in sequence:
        if i == 0:
            new_sequence.append(1)
        elif len(str(i)) % 2 == 0:
            first, second = str(i), str(i)
            first = int(first[:len(first) // 2])
            second = int(second[len(second) // 2:])
            new_sequence.extend([first, second])
        else:
            new_sequence.append(i * 2024)
    return blink(new_sequence, steps - 1)


def fast_blink(occurrences: defaultdict[int, int], steps=1):
    if steps == 0:
        return occurrences
    new_occurrences = defaultdict(int)
    for i, occurrence in occurrences.items():
        if i == 0:
            new_occurrences[1] += occurrence
        elif len(str(i)) % 2 == 0:
            first, second = str(i), str(i)
            first = int(first[:len(first) // 2])
            second = int(second[len(second) // 2:])
            new_occurrences[first] += occurrence
            new_occurrences[second] += occurrence
        else:
            new_occurrences[i * 2024] += occurrence

    return fast_blink(new_occurrences, steps - 1)


# Helper to show elapsed time of part 2 (naive)
def print_elapsed(task_name, start_time, stop_event):
    while True:
        elapsed = time.perf_counter() - start_time
        print(f"\r{task_name}: {elapsed:.2f}s elapsed", end="")
        if stop_event.is_set():
            break
        time.sleep(0.1)  # Update interval (adjust as needed)


def part1_slow():
    start = time.perf_counter()
    sequence = get_data()
    result = len(blink(sequence, 25))
    end = time.perf_counter()
    print(f"Part 1 (slow): {result} ({end - start:.4f}s)")


def part2_slow():
    sequence = get_data()
    # Blocking code
    start = time.perf_counter()
    stop_event = threading.Event()
    t = threading.Thread(target=print_elapsed, args=("Part 2 (slow)", start, stop_event))
    t.start()
    try:
        result = len(blink(sequence, 75))  # Your blocking code
    finally:
        stop_event.set()
        t.join()  # Wait for the thread to finish

    end = time.perf_counter()
    print(f"\rPart 2 (slow): {result} ({end - start:.4f}s)")


def part1_fast():
    start = time.perf_counter()
    sequence = get_data()
    occurrences = defaultdict(int)
    for i in sequence:
        occurrences[i] += 1
    result = sum(fast_blink(occurrences, 25).values())
    end = time.perf_counter()
    print(f"Part 1 (fast): {result} ({end - start:.4f}s)")


def part2_fast():
    start = time.perf_counter()
    sequence = get_data()
    occurrences = defaultdict(int)
    for i in sequence:
        occurrences[i] += 1
    result = sum(fast_blink(occurrences, 75).values())
    end = time.perf_counter()
    print(f"Part 2 (fast): {result} ({end - start:.4f}s)")


if __name__ == "__main__":
    part1_fast()
    part1_slow()
    part2_fast()
    part2_slow()
