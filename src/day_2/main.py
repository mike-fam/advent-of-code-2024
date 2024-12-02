from itertools import combinations


def part1():
    safe_count = 0
    with open("input.txt") as fin:
        for line in fin:
            parsed_line = list(map(int, line.strip().split()))
            valid = part1_validate(parsed_line)
            if valid:
                safe_count += 1
    print("Part 1:", safe_count)


def part1_validate(nums):
    previous = None
    ascending = None
    for current in nums:
        if previous is None:
            previous = current
            continue
        
        if not (1 <= abs(current - previous) <= 3):
            return False
            
        if ascending is None:
            ascending = current > previous
            previous = current
            continue
        
        if (current > previous) is not ascending:
            return False
        previous = current
    return True
            

def part2():
    safe_count = 0
    with open("input.txt") as fin:
        for line in fin:
            parsed_line = list(map(int, line.strip().split()))

            # Pick a way to run this
            # valid = part2_validate_bruteforce(list(map(int, line.strip().split())), True)
            # valid = part2_validate_efficient(list(map(int, line.strip().split())), True)
            valid = (
                part2_validate_efficient_nicer(parsed_line, True) or
                part2_validate_efficient_nicer(list(reversed(parsed_line)), True))
            if valid:
                safe_count += 1
    print("Part 2:", safe_count)


# O(n) (O(4n) to be exact), not very elegant
def part2_validate_efficient(nums: list[int], tolerable=False):
    previous = None
    ascending = None
    for index, current in enumerate(nums):
        if previous is None:
            previous = current
            continue

        if not (1 <= abs(current - previous) <= 3):
            if not tolerable:
                return False
            # Assume that problematic number is either at index, index - 1, or index - 2
            return (
                part2_validate_efficient(nums[:index] + nums[index + 1:]) or
                part2_validate_efficient(nums[:index - 1] + nums[index:]) or
                part2_validate_efficient(nums[:index - 2] + nums[index - 1:])
            )
            
        if ascending is None:
            ascending = current > previous
            previous = current
            continue
        
        if (current > previous) is not ascending:
            if not tolerable:
                return False
            # Assume that problematic number is either at index, index - 1, or index - 2
            return (
                part2_validate_efficient(nums[:index] + nums[index + 1:]) or
                part2_validate_efficient(nums[:index - 1] + nums[index:]) or
                part2_validate_efficient(nums[:index - 2] + nums[index - 1:])
            )

        previous = current
    return True


# O(n) (O(4n) to be exact), a bit more elegant
def part2_validate_efficient_nicer(nums: list[int], tolerable=False):
    previous = None
    ascending = None
    for index, current in enumerate(nums):
        if previous is None:
            previous = current
            continue

        if not (1 <= abs(current - previous) <= 3):
            if not tolerable:
                return False
            return part2_validate_efficient_nicer(nums[:index] + nums[index + 1:])
            
        if ascending is None:
            ascending = current > previous
            previous = current
            continue
        
        if (current > previous) is not ascending:
            if not tolerable:
                return False
            return part2_validate_efficient_nicer(nums[:index] + nums[index + 1:])


        previous = current
    return True


# O(n^2)
def part2_validate_bruteforce(nums, tolerable=False):
    previous = None
    ascending = None
    for index, current in enumerate(nums):
        if previous is None:
            previous = current
            continue
        
        if not (1 <= abs(current - previous) <= 3):
            if tolerable:
                for combination in combinations(nums, len(nums) - 1):
                    if part2_validate_bruteforce(combination):
                        return True
            return False
            
        if ascending is None:
            ascending = current > previous
            previous = current
            continue
        
        if (current > previous) is not ascending:
            if tolerable:
                for combination in combinations(nums, len(nums) - 1):
                    if part2_validate_bruteforce(combination):
                        return True
            return False

        previous = current
    return True


def part2_validate_raf(nums):
    if len(nums) < 2:
        return 0
    unsafe = 0
    increasing = nums[1] - nums[0] > 0
    for i in range(len(nums) - 1):
        delta = nums[i + 1] - nums[i] * (1 if increasing else -1)
        if delta < 1 or delta > 3:
            unsafe += 1
    return unsafe <= 1


if __name__ == "__main__":
    part1()
    part2()
