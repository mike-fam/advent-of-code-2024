from enum import Enum

def get_input():
    with open("input.txt") as fin:
        return fin.read()


def process_plain_text(text, pattern):
    if text.startswith(pattern):
        return True, len(pattern), pattern
    return False, 0, None


def process_mul(text):
    return process_plain_text(text, "mul(")


def process_comma(text):
    return process_plain_text(text, ",")


def process_close(text):
    return process_plain_text(text, ")")


def process_arg(text):
    # Maximum 3 characters
    if not text[0].isdecimal():
        return False, 0, None
    digits = text[0]
    for i in range(1, 3):
        potential_digit = text[i]
        if not potential_digit.isdecimal():
            return True, i, int(digits)
        digits += potential_digit
    return True, 3, int(digits)
    

def find_next_mul(text):
    process_funcs = [process_mul, process_arg, process_comma, process_arg, process_close]
    pointer = 0
    while pointer < len(text):
        found = None
        for process_index, process_func in enumerate(process_funcs):
            valid, next_pointer_delta, result = process_func(text[pointer:])
            # invalid, move to next character
            if not valid:
                pointer += 1
                found = None
                break

            # valid
            if process_index == 0:
                found = []
            
            pointer += next_pointer_delta
            found.append(result)
            
            
        if found is not None:
            return found, pointer
    return None, len(text)


def find_next_do_dont(text):
    next_do = text.find("do()")
    next_dont = text.find("don't()")
    if next_do == -1 and next_dont == -1:
        return None, len(text)
    if next_do != -1 and next_dont == -1:
        return True, next_do + 4
    if next_dont != -1 and next_do == -1:
        return False, next_dont + 7
    if next_do != -1 and next_dont != -1:
        return next_do < next_dont, min(next_do, next_dont) + (4 if next_do < next_dont else 7)


# O(n) worst case
def part1():
    text = get_input()
    pointer = 0
    expressions_found = []
    while True:
        found, next_pointer_delta = find_next_mul(text[pointer:])
        if found is None:
            break
        pointer += next_pointer_delta
        expressions_found.append(found)
    
    total = 0
    for _, arg1, _, arg2, _ in expressions_found:
        total += arg1 * arg2
    print("Part 1", total)


# O(n^2) worst case
def part2():
    text = get_input()
    activated = True
    pointer = 0
    expressions_found = []
    while True:
        new_activated, next_activation_pointer_delta = find_next_do_dont(text[pointer:])
        mul_found, next_mul_pointer_delta = find_next_mul(text[pointer:])
        
        if mul_found is None:
            break
        
        if not activated or next_activation_pointer_delta < next_mul_pointer_delta:
            pointer += next_activation_pointer_delta
            activated = new_activated
            continue
        pointer += next_mul_pointer_delta
        expressions_found.append(mul_found)
        
    total = 0
        
    for _, arg1, _, arg2, _ in expressions_found:
        total += arg1 * arg2
    print("Part 2", total)


if __name__ == "__main__":
    part1()
    part2()
