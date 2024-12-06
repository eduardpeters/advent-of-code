def solve(path: str, part: int) -> None:
    letters = load_file(path)
    print(letters)
    if part == 1:
        print("Solving for part 1")
    else:
        print("Solving for part 2")


def load_file(path: str):
    letters_matrix: list[list[str]] = []
    with open(path) as file:
        for line in file:
            letters_matrix.append([*line.strip()])
    return letters_matrix


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
