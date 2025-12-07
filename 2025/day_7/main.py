START = "S"
FREE = "."
SPLITTER = "^"
TACHYON = "|"


def count_splits(grid: list[list[str]], t_row: int, t_column: int) -> int:
    # Out of Bounds, no splitting can occur and no further travel possible
    if t_row < 0 or t_row >= len(grid) or t_column < 0 or t_column >= len(grid[t_row]):
        return 0

    #  If entering an existing path, leave it to the other branch
    if grid[t_row][t_column] == TACHYON:
        return 0

    if grid[t_row][t_column] == FREE:
        # No splitting, travels straight down
        grid[t_row][t_column] = TACHYON
        return count_splits(grid, t_row + 1, t_column)

    grid[t_row][t_column - 1] = TACHYON
    grid[t_row][t_column + 1] = TACHYON

    return (
        1
        + count_splits(grid, t_row + 1, t_column - 1)
        + count_splits(grid, t_row + 1, t_column + 1)
    )


def solve(path: str, part: int) -> None:
    grid = load_file(path)

    if part == 1:
        print("Solving for part 1")
        start_column = grid[0].index(START)
        start_row = 1
        print(f"Starting tachyon tracking on column {start_column}")
        split_count = count_splits(grid, start_row, start_column)
        print(f"Trachyon split {split_count} times!")
    else:
        print("Solving for part 2")


def load_file(path: str) -> list[list[str]]:
    grid: list[list[str]] = []

    with open(path) as file:
        for line in file:
            grid.append(list(line.strip()))

    return grid


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
