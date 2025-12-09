def side_length(a: int, b: int) -> int:
    return abs(a - b) + 1


def rectangle_area(a: tuple[int, int], b: tuple[int, int]) -> int:
    return side_length(a[0], b[0]) * side_length(a[1], b[1])


def solve(path: str, part: int) -> None:
    tiles = load_file(path)

    if part == 1:
        print("Solving for part 1")
        max_area = 0
        for i, pivot in enumerate(tiles):
            for opposite in tiles[i + 1 :]:
                area = rectangle_area(pivot, opposite)
                if area > max_area:
                    max_area = area
        print(f"Max area found: {max_area}")
    else:
        print("Solving for part 2")


def load_file(path: str) -> list[tuple[int, int]]:
    tiles: list[tuple[int, int]] = []

    with open(path) as file:
        for line in file:
            x, y = line.strip().split(",")
            tiles.append((int(x), int(y)))

    return tiles


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
