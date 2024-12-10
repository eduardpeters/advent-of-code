from enum import Enum

EMPTY = "."
GUARD = "^"
OBSTRUCTION = "#"
VISITED = "X"


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def solve(path: str, part: int) -> None:
    area = load_file(path)
    for row in area:
        print(row)
    starting_position = get_starting_position(area)
    starting_direction = Direction.UP
    if part == 1:
        print("Solving for part 1")
        print(starting_position)
        positions_visited = get_patrolled_positions(
            area, starting_position, starting_direction
        )
        print(f"Guard visited: {positions_visited} positions")
    else:
        print("Solving for part 2")
        new_obstruction_positions = get_new_obstruction_positions(
            area, starting_position, starting_direction
        )
        print(f"Found {len(new_obstruction_positions)} positions that create loops")


def get_new_obstruction_positions(
    area: list[list[str]],
    starting_position: tuple[int, int],
    starting_direction: Direction,
) -> list[tuple[int, int]]:
    obstruction_positions: list[tuple[int, int]] = []

    for row in range(0, len(area)):
        for column in range(0, len(area[row])):
            position_content = area[row][column]
            if position_content != EMPTY:
                continue
            area[row][column] = OBSTRUCTION
            if is_in_a_loop(area, starting_position, starting_direction):
                obstruction_positions.append((row, column))
            area[row][column] = EMPTY
            print(
                f"Checked: ({row},{column}) new positions: {len(obstruction_positions)}"
            )

    return obstruction_positions


def is_in_a_loop(
    area: list[list[str]],
    starting_position: tuple[int, int],
    starting_direction: Direction,
) -> bool:
    visit_history: dict[tuple[int, int], list[Direction]] = {}

    current_position = starting_position
    current_direction = starting_direction
    while 0 <= current_position[0] < len(area) and 0 <= current_position[1] < len(
        area[current_position[0]]
    ):
        if current_position in visit_history:
            visit_history[current_position].append(current_direction)
        else:
            visit_history[current_position] = [current_direction]

        next_position = move_forward(current_position, current_direction)
        if (
            next_position[0] < 0
            or next_position[0] >= len(area)
            or next_position[1] < 0
            or next_position[1] >= len(area[next_position[0]])
        ):
            # Guard has stepped out of bounds, no loop
            return False
        if (
            next_position in visit_history
            and current_direction in visit_history[next_position]
        ):
            # Guard has walked this path before, is a loop
            return True

        next_position_content = area[next_position[0]][next_position[1]]
        if next_position_content == OBSTRUCTION:
            current_direction = turn_right(current_direction)
        else:
            current_position = next_position
    # Guard has stepped out of bounds, no loop
    return False


def get_patrolled_positions(
    area: list[list[str]],
    starting_position: tuple[int, int],
    starting_direction: Direction,
) -> int:
    visited = 1

    current_position = starting_position
    current_direction = starting_direction
    while 0 <= current_position[0] < len(area) and 0 <= current_position[1] < len(
        area[current_position[0]]
    ):
        next_position = move_forward(current_position, current_direction)
        if (
            next_position[0] < 0
            or next_position[0] >= len(area)
            or next_position[1] < 0
            or next_position[1] >= len(area[next_position[0]])
        ):
            # Guard has stepped out of bounds
            return visited
        next_position_content = area[next_position[0]][next_position[1]]
        if next_position_content == OBSTRUCTION:
            current_direction = turn_right(current_direction)
        else:
            # Only count if not visited yet and mark it
            if area[current_position[0]][current_position[1]] != VISITED:
                visited += 1
                area[current_position[0]][current_position[1]] = VISITED
            current_position = next_position

    return visited


def turn_right(current_direction: Direction) -> Direction:
    match current_direction:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP


def move_forward(
    current_position: tuple[int, int], current_direction: Direction
) -> tuple[int, int]:
    match current_direction:
        case Direction.UP:
            return (current_position[0] - 1, current_position[1])
        case Direction.DOWN:
            return (current_position[0] + 1, current_position[1])
        case Direction.RIGHT:
            return (current_position[0], current_position[1] + 1)
        case Direction.LEFT:
            return (current_position[0], current_position[1] - 1)


def get_starting_position(area: list[list[str]]) -> tuple[int, int]:
    for row in range(0, len(area)):
        for column, position in enumerate(area[row]):
            if position == GUARD:
                return row, column
    return (0, 0)


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
