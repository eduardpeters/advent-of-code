import re
from math import log10


def count_digits(number: int) -> int:
    if number > 0:
        digits = int(log10(number)) + 1
    elif number == 0:
        digits = 1
    else:
        digits = int(log10(-number)) + 1

    return digits


def solve(path: str, part: int) -> None:
    ranges = load_file(path)

    sum = 0
    if part == 1:
        print("Solving for part 1")
        for range in ranges:
            lower_str, upper_str = range.split("-")
            lower = int(lower_str)
            upper = int(upper_str)
            i = lower
            while i <= upper:
                if count_digits(i) % 2 != 0:
                    i += 1
                    continue
                id = str(i)
                if id[: len(id) // 2] == id[len(id) // 2 :]:
                    print("Found invalid:", id)
                    sum += i
                i += 1
    else:
        print("Solving for part 2")
        expr = re.compile("^(\\d+)\\1+$")
        for range in ranges:
            lower_str, upper_str = range.split("-")
            lower = int(lower_str)
            upper = int(upper_str)
            i = lower
            while i <= upper:
                id = str(i)
                if re.match(expr, id):
                    print("Found invalid:", id)
                    sum += i
                i += 1

    print("Sum:", sum)


def load_file(path: str) -> list[str]:
    ranges: list[str] = []
    with open(path) as file:
        ranges = file.read().split(",")
    return ranges


def choose_action():
    choice = int(input("0. Example One\n1. Part One\n2. Example Two\n3. Part Two\n-> "))
    if choice == 0:
        print("Running example part 1")
        solve("example.txt", 1)
    elif choice == 1:
        print("Running input part 1")
        solve("input.txt", 1)
    elif choice == 2:
        print("Running example part 2")
        solve("example.txt", 2)
    else:
        print("Running input part 2")
        solve("input.txt", 2)


if __name__ == "__main__":
    choose_action()
