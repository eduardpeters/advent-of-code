EMPTY = "."
CLEARED = "x"
ROLL = "@"
MOVABLE_THRESHOLD = 4


def count_surrounding(map: list[str], row: int, column: int) -> int:
    if map[row][column] != ROLL:
        return 0
    # Map is padded, so we should not be checking at or beyond the bounds
    if row <= 0 or row >= len(map) or column <= 0 or column >= len(map[row]):
        return 0

    count = 0
    check_column = column - 1
    while check_column <= column + 1:
        # Check row above
        if map[row - 1][check_column] == ROLL:
            count += 1
        # Check row below
        if map[row + 1][check_column] == ROLL:
            count += 1
        check_column += 1
    # Check sides
    if map[row][column - 1] == ROLL:
        count += 1
    if map[row][column + 1] == ROLL:
        count += 1

    return count


def solve(path: str, part: int) -> None:
    map = load_file(path)

    if part == 1:
        print("Solving for part 1")
        movable_count = 0
        row = 1
        while row < len(map) - 1:
            column = 1
            while column < len(map[row]) - 1:
                if map[row][column] == ROLL:
                    surrounding_count = count_surrounding(map, row, column)
                    if surrounding_count < MOVABLE_THRESHOLD:
                        movable_count += 1
                column += 1

            row += 1

        print(f"Movable count: {movable_count}")
    else:
        print("Solving for part 2")
        removed_count = 0
        row = 1
        while row < len(map) - 1:
            column = 1
            while column < len(map[row]) - 1:
                if map[row][column] == ROLL:
                    surrounding_count = count_surrounding(map, row, column)
                    if surrounding_count < MOVABLE_THRESHOLD:
                        # Remove from grid
                        map[row] = map[row][:column] + CLEARED + map[row][column + 1 :]
                        removed_count += 1
                        # Go back to previous row and clear any newly available
                        row -= 2
                        break
                column += 1

            row += 1

        print(f"Removed count: {removed_count}")


def load_file(path: str) -> list[str]:
    map: list[str] = []
    with open(path) as file:
        for line in file:
            padded_line = EMPTY + line.strip() + EMPTY
            map.append(padded_line)
    padding_line = EMPTY * len(map[0])
    map.insert(0, padding_line)
    map.append(padding_line)
    return map


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
