def solve(path: str, part: int) -> None:
    if part == 1:
        file_string = load_file(path)
        potential_matches = get_potential_multiplications(file_string)
        print(potential_matches)


def load_file(path: str) -> str:
    with open(path) as file:
        file_string = file.read()
    return file_string


def get_potential_multiplications(file_string: str) -> list[str]:
    split_string = file_string.split("mul")
    if not file_string.startswith("mul"):
        split_string = split_string[1:]
    return split_string


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
