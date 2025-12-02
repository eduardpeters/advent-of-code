MIN_POSITION = 0
MAX_POSITION = 99
START_POSITION = 50

DIRECTION_LEFT = "L"
DIRECTION_RIGHT = "R"


def get_rotation_components(rotation: str) -> tuple[str, int]:
    direction = rotation[0]
    magnitude = int(rotation[1:])
    return (direction, magnitude)


def apply_rotation(current_position: int, rotation: str) -> tuple[int, int]:
    direction, magnitude = get_rotation_components(rotation)
    zero_clicks = 0
    print("Rotating", direction, magnitude)

    if direction == DIRECTION_LEFT:
        movements = -magnitude
        movements_to_zero = current_position
    else:
        movements = magnitude
        if current_position == 0:
            movements_to_zero = 0
        else:
            movements_to_zero = MAX_POSITION + 1 - current_position

    tmp = current_position + movements
    if magnitude >= movements_to_zero:
        if current_position != 0:
            zero_clicks += 1
        zero_clicks += (magnitude - movements_to_zero) // (MAX_POSITION + 1)
    final_position = tmp % (MAX_POSITION + 1)

    return final_position, zero_clicks


def solve(path: str, part: int) -> None:
    rotations = load_file(path)

    if part == 1:
        print("Solving for part 1")
        zero_count = 0
        position = START_POSITION
        for rotation in rotations:
            print(f"Before position: {position}")
            position, _ = apply_rotation(position, rotation)
            print(f"After position: {position}")
            if position == 0:
                zero_count += 1
        print(f"Zero count: {zero_count}")
    else:
        print("Solving for part 2")
        zero_count = 0
        zero_clicks = 0
        position = START_POSITION
        for rotation in rotations:
            print(f"Before position: {position}")
            position, clicks = apply_rotation(position, rotation)
            print(f"After position: {position}")
            if position == 0:
                zero_count += 1
            zero_clicks += clicks
        print(f"Zero count: {zero_count}")
        print(f"Zero clicks: {zero_clicks}")
        print(f"Total: {zero_count + zero_clicks}")


def load_file(path: str) -> list[str]:
    rotations: list[str] = []
    with open(path) as file:
        for line in file:
            rotations.append(line.strip())
    return rotations


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
