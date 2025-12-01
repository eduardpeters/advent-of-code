MIN_POSITION = 0
MAX_POSITION = 99
START_POSITION = 50

DIRECTION_LEFT = "L"
DIRECTION_RIGHT = "R"


def apply_rotation(current_position: int, rotation: str) -> int:
    direction = rotation[0]
    magnitude = int(rotation[1:])
    print("Rotating", direction, magnitude)
    # Full rotations
    while magnitude >= MAX_POSITION + 1:
        magnitude -= MAX_POSITION + 1

    if direction == DIRECTION_RIGHT:
        return (current_position + magnitude) % (MAX_POSITION + 1)
    if magnitude > current_position:
        # Go to 99
        magnitude -= current_position + 1
        current_position = MAX_POSITION

    return current_position - magnitude


def solve(path: str, part: int) -> None:
    rotations = load_file(path)
    print(rotations)
    if part == 1:
        print("Solving for part 1")
        zero_count = 0
        position = START_POSITION
        for rotation in rotations:
            print(f"Before position: {position}")
            position = apply_rotation(position, rotation)
            print(f"After position: {position}")
            if position == 0:
                zero_count += 1
        print(f"Zero count: {zero_count}")
    else:
        print("Solving for part 2")


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
