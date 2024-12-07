XMAS = "XMAS"


def solve(path: str, part: int) -> None:
    letters = load_file(path)
    print(letters)
    if part == 1:
        print("Solving for part 1")
        xmas_count = count_xmas(letters)
        print(f"Found XMAS {xmas_count} times")
    else:
        print("Solving for part 2")


def count_xmas(letters: list[list[str]]):
    count = 0
    for i_row, row in enumerate(letters):
        for i_col, _ in enumerate(row):
            count += count_square(letters, i_row, i_col, XMAS)
    return count


def count_square(letters: list[list[str]], row: int, column: int, word: str) -> int:
    if not word:
        return 1
    if letters[row][column] != word[0]:
        return 0

    # print(f"Entering recursion at ({row, column})={letters[row][column]} for {word}")
    count = 0
    look_behind, look_forward, look_above, look_below = check_bounds(
        letters, row, column, len(word)
    )

    word_slice = word[1:]

    if look_behind:
        count += count_line(letters, row, column - 1, 0, -1, word_slice)
    if look_forward:
        count += count_line(letters, row, column + 1, 0, 1, word_slice)

    return count


def count_line(
    letters: list[list[str]],
    row: int,
    column: int,
    row_step: int,
    column_step: int,
    word: str,
) -> int:
    if not word:
        return 1
    if letters[row][column] != word[0]:
        return 0
    return count_line(
        letters, row + row_step, column + column_step, row_step, column_step, word[1:]
    )


def check_bounds(
    letters: list[list[str]], row: int, column: int, word_length: int
) -> tuple[int, int, int, int]:
    row_count = len(letters)
    column_count = len(letters[column])

    look_behind = column >= word_length - 1
    look_forward = column + word_length - 1 < column_count
    look_above = row >= word_length - 1
    look_below = row + word_length - 1 < row_count

    return look_behind, look_forward, look_above, look_below


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
