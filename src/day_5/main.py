import time
from functools import wraps

def timed(func):
    """
    A decorator that prints the time a function takes to execute.
    """

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
    updates = []
    graph = {}
    section = 1
    with open("input.txt") as fin:
        for line in fin:
            line = line.strip()
            if line == "":
                section = 2
                continue
            if section == 1:
                before, after = line.split("|")
                before, after = int(before), int(after)
                if before not in graph:
                    graph[before] = []
                if after not in graph:
                    graph[after] = []
                graph[before].append(after)
            elif section == 2:
                updates.append(list(map(int, line.split(","))))
    return graph, updates
            

def is_update_valid(graph, update):
    prohibited = set()
    for page in reversed(update):
        if page in prohibited:
            return False
        prohibited.update(graph.get(page, []))
    return True


@timed
def part1():
    graph, updates = get_data()
    valid_updates = []
    for update in updates:
        if is_update_valid(graph, update):
            valid_updates.append(update)
        
    total = 0
    for valid_update in valid_updates:
        total += valid_update[len(valid_update) // 2]
    print("Part 1:", total)


def merge(l1, l2, key):
    pointer1 = pointer2 = 0
    merged = []
    while len(merged) < len(l1) + len(l2):
        if pointer1 == len(l1):
            merged.extend(l2[pointer2:])
            break
        if pointer2 == len(l2):
            merged.extend(l1[pointer1:])
            break
        if key(l1[pointer1], l2[pointer2]) >= 0:
            merged.append(l1[pointer1])
            pointer1 += 1
        else:
            merged.append(l2[pointer2])
            pointer2 += 1
    return merged


# merge sort for a stable sort
def mergesort(l, key):
    if len(l) <= 1:
        return l
    middle = len(l) // 2
    return merge(mergesort(l[:middle], key), mergesort(l[middle:], key), key)


@timed
def part2_slow():
    graph, updates = get_data()
    valid_updates = []
    for update in updates:
        prohibited = set()
        fixed = False
        fixed_update = []
        for i, page in enumerate(reversed(update)):
            fixed_update.append(page)
            prohibited.update(graph.get(page, []))
            if page in prohibited:
                fixed = True
                swap_index = i
                while not is_update_valid(graph, list(reversed(fixed_update))):
                    fixed_update[swap_index], fixed_update[swap_index - 1] = fixed_update[swap_index - 1], fixed_update[swap_index]
                    swap_index -= 1
        if fixed:
            valid_updates.append(list(reversed(fixed_update)))

    total = 0
    for valid_update in valid_updates:
        total += valid_update[len(valid_update) // 2]
    print("Part 2 - Slow:", total)


@timed
def part2():
    graph, updates = get_data()
    valid_updates = []
    def sortkey(a, b):
        if b in graph.get(a, set()):
            return 1
        if a in graph.get(b, set()):
            return -1
        return 0
    for update in updates:
        if not is_update_valid(graph, update):
            sorted_update = mergesort(update, sortkey)
            valid_updates.append(sorted_update)
    total = 0
    for valid_update in valid_updates:
        total += valid_update[len(valid_update) // 2]
    print("Part 2:", total)



if __name__ == "__main__":
    part1()
    part2()
    part2_slow()
