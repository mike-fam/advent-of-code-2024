from itertools import combinations


def part1():
    safe_count = 0
    with open("input.txt") as fin:
        for line in fin:
            valid = part1_validate(list(map(int, line.strip().split())))
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
            valid = part2_validate_efficient(list(map(int, line.strip().split())), True)
            if valid:
                safe_count += 1
    print("Part 2:", safe_count)


# O(n), not very elegant
def part2_validate_efficient(nums: list[int], toleratable=False):
    previous = None
    ascending = None
    for index, current in enumerate(nums):
        if previous is None:
            previous = current
            continue
        
        if not (1 <= abs(current - previous) <= 3):
            if not toleratable:
                return False
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
            if not toleratable:
                return False
            return (
                part2_validate_efficient(nums[:index] + nums[index + 1:]) or
                part2_validate_efficient(nums[:index - 1] + nums[index:]) or
                part2_validate_efficient(nums[:index - 2] + nums[index - 1:])
            )


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

if __name__ == "__main__":
    part1()
    part2()
