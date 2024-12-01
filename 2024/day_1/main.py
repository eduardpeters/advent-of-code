def solve(path: str, part: int) -> None:
    left_column, right_column = get_columns_from_file(path)
    if part == 1:
        print("Sorting and Adding Distances")
        left_column.sort()
        right_column.sort()
        total = get_total_distance(left_column, right_column)
        print(f"Total Distance: {total}")


def get_columns_from_file(path: str) -> tuple[list[int], list[int]]:
    left_column: list[int] = []
    right_column: list[int] = []
    with open(path) as input_file:
        for line in input_file:
            columns = line.split()
            left_column.append(int(columns[0]))
            right_column.append(int(columns[1]))
    return left_column, right_column


def get_total_distance(left_column: list[int], right_column: list[int]) -> int:
    total = 0
    for a, b in zip(left_column, right_column):
        total += a - b if a > b else b - a
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
