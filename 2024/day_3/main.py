import re


def solve(path: str, part: int) -> None:
    file_string = load_file(path)
    if part == 1:
        potential_matches = get_potential_multiplications(file_string)
    else:
        do_string = get_do_instructions(file_string)
        potential_matches = get_potential_multiplications(do_string)

    print(f"Potential matches: {len(potential_matches)}")
    matches = get_valid_multiplications(potential_matches)
    print(f"Actual matches: {len(matches)}")
    result = add_multiplications(matches)
    print(f"Valid multiplications add up to: {result}")


def load_file(path: str) -> str:
    with open(path) as file:
        file_string = file.read()
    return file_string


def get_do_instructions(file_string: str) -> str:
    split = file_string.split("do()")

    do_instructions: list[str] = []
    for string in split:
        re_split = string.split("don't()")
        do_instructions.append(re_split[0])

    return "".join(do_instructions)


def get_potential_multiplications(file_string: str) -> list[str]:
    split_string = file_string.split("mul")
    if not file_string.startswith("mul"):
        split_string = split_string[1:]
    return split_string


def get_valid_multiplications(candidates: list[str]) -> list[tuple[int, int]]:
    valid_arguments: list[tuple[int, int]] = []
    for candidate in candidates:
        arguments = re.match("\\((\\d{1,3},\\d{1,3})\\)", candidate)
        if not arguments:
            continue
        match = arguments.group(1)
        split_arguments = match.split(",")
        valid_arguments.append((int(split_arguments[0]), int(split_arguments[1])))
    return valid_arguments


def add_multiplications(arguments: list[tuple[int, int]]) -> int:
    total = 0
    for pair in arguments:
        total += pair[0] * pair[1]
    return total


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
