def part1():
    firsts = []
    seconds = []
    with open("input.txt") as fin:
        for line in fin:
            first, second = line.strip().split()
            first = int(first)
            second = int(second)
            firsts.append(first)
            seconds.append(second)
    sorted_firsts = sorted(firsts)
    sorted_seconds = sorted(seconds)
    min_len = min(len(sorted_firsts), len(sorted_seconds))
    total = 0
    for i, j in zip(sorted_firsts[:min_len], sorted_seconds[:min_len]):
        total += abs(i - j)
    print(total)


def part2():
    occurences = {}
    with open("input.txt") as fin:
        for line in fin:
            first, second = line.strip().split()
            first = int(first)
            second = int(second)
            first_occ_first_col, first_occ_second_col = occurences.get(first, (0, 0))
            occurences[first] = (first_occ_first_col + 1, first_occ_second_col)
            second_occ_first_col, second_occ_second_col = occurences.get(second, (0, 0))
            occurences[second] = (second_occ_first_col, second_occ_second_col + 1)
    total = 0
    for i, (occ_first_col, occ_second_col) in occurences.items():
        total += i * occ_first_col * occ_second_col
    print(total)

if __name__ == "__main__":
    part2()
