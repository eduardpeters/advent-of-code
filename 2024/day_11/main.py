from math import log10


def solve(path: str, part: int) -> None:
    stones = load_file(path)
    print(stones)
    if part == 1:
        print("Solving for part 1")
        blinks = 25
        count = count_after_blinks(stones, blinks)
        print(f"Stones after {blinks} blinks: {count}")
    else:
        print("Solving for part 2")


def count_after_blinks(stones: list[int], n_blinks: int) -> int:
    current_stones = stones
    for _ in range(n_blinks):
        new_stones: list[int] = []
        for stone in current_stones:
            blink_result = blink(stone)
            new_stones.extend(blink_result)
        current_stones = new_stones
    return len(current_stones)


def blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    digits = count_digits(stone)
    if digits % 2 == 0:
        factor = 10 ** (digits // 2)
        left_split = stone // factor
        right_split = stone - left_split * factor
        return [left_split, right_split]
    return [stone * 2024]


def count_digits(number: int) -> int:
    if number > 0:
        digits = int(log10(number)) + 1
    elif number == 0:
        digits = 1
    else:
        digits = int(log10(-number)) + 1

    return digits


def load_file(path: str) -> list[int]:
    stones: list[int] = []
    with open(path) as file:
        stones = [int(stone) for stone in file.readline().split()]
    return stones


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
