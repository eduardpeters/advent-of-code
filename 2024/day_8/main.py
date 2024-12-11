EMPTY = "."


def solve(path: str, part: int) -> None:
    area = load_file(path)
    if part == 1:
        print("Solving for part 1")
        antinodes = get_antinodes(area, with_harmonics=False)
    else:
        print("Solving for part 2")
        antinodes = get_antinodes(area, with_harmonics=True)
    print(f"Found {len(antinodes)} antinodes")


def get_antinodes(area: list[list[str]], with_harmonics: bool) -> set[tuple[int, int]]:
    antinodes: set[tuple[int, int]] = set()
    for row in range(0, len(area)):
        for column in range(0, len(area[row])):
            current_content = area[row][column]
            if current_content == EMPTY:
                continue
            new_antinodes = find_matching_antennae_nodes(
                area, (row, column), current_content, with_harmonics
            )
            antinodes.update(new_antinodes)

    return antinodes


def find_matching_antennae_nodes(
    area: list[list[str]],
    starting_position: tuple[int, int],
    antenna_type: str,
    with_harmonics: bool,
) -> list[tuple[int, int]]:
    antinodes: list[tuple[int, int]] = []
    for row in range(starting_position[0], len(area)):
        for column in range(
            starting_position[1] + 1 if row == starting_position[0] else 0,
            len(area[row]),
        ):
            if area[row][column] == antenna_type:
                if with_harmonics:
                    # Add matching antenna positions
                    antinodes.extend([starting_position, (row, column)])
                candidates = get_antinode_candidates(
                    area, starting_position, row, column, with_harmonics
                )
                for candidate in candidates:
                    if is_inside_bounds(area, candidate):
                        antinodes.append(candidate)

    return antinodes


def get_antinode_candidates(
    area: list[list[str]],
    starting_position: tuple[int, int],
    current_row: int,
    current_column: int,
    with_harmonics: bool,
) -> list[tuple[int, int]]:
    row_difference = current_row - starting_position[0]
    column_difference = current_column - starting_position[1]
    if with_harmonics:
        candidates: list[tuple[int, int]] = []
        iterations = 1
        while True:
            new_antinode = (
                starting_position[0] - row_difference * iterations,
                starting_position[1] - column_difference * iterations,
            )
            if not is_inside_bounds(area, new_antinode):
                break
            candidates.append(new_antinode)
            iterations += 1
        iterations = 1
        while True:
            new_antinode = (
                starting_position[0] + row_difference * iterations,
                starting_position[1] + column_difference * iterations,
            )
            if not is_inside_bounds(area, new_antinode):
                break
            candidates.append(new_antinode)
            iterations += 1
    else:
        candidate_one = (
            starting_position[0] - row_difference,
            starting_position[1] - column_difference,
        )
        candidate_two = (
            current_row + row_difference,
            current_column + column_difference,
        )
        candidates = [candidate_one, candidate_two]

    return candidates


def is_inside_bounds(area: list[list[str]], antinode: tuple[int, int]) -> bool:
    if not 0 <= antinode[0] < len(area):
        return False
    if not 0 <= antinode[1] < len(area[antinode[0]]):
        return False
    return True


def load_file(path: str) -> list[list[str]]:
    area: list[list[str]] = []

    with open(path) as file:
        for line in file:
            trimmed_line = line.strip()
            area.append(list(trimmed_line))
    return area


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
