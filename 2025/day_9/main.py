from dataclasses import dataclass


@dataclass
class Node:
    position: tuple[int, int]
    next: "Node | None" = None
    prev: "Node | None" = None


def side_length(a: int, b: int) -> int:
    return abs(a - b) + 1


def rectangle_area(a: tuple[int, int], b: tuple[int, int]) -> int:
    return side_length(a[0], b[0]) * side_length(a[1], b[1])


def is_on_perimeter(perimeter: Node, x: tuple[int, int]) -> bool:
    if not perimeter.next:
        return False
    a = perimeter.position
    b = perimeter.next.position
    if a[0] == b[0] and a[0] == x[0]:
        if a[1] < x[1] < b[1] or a[1] > x[1] > b[1]:
            return True
    if a[1] == b[1] and a[1] == x[1]:
        if a[0] < x[0] < b[0] or a[0] > x[0] > b[0]:
            return True
    return False


def build_perimeter(tiles: list[tuple[int, int]]) -> Node:
    base_node = Node(position=tiles[0])
    current_node = base_node
    for tile in tiles[1:]:
        current_node.next = Node(position=tile, prev=current_node)
        current_node = current_node.next

    current_node.next = base_node
    base_node.prev = current_node

    return base_node


def get_final_rectangle_vertex(
    a: tuple[int, int], b: tuple[int, int], c: tuple[int, int]
) -> tuple[int, int]:
    vertex_position: tuple[int, int] = (0, 0)
    if a[0] == b[0]:
        vertex_position = (c[0], a[1])
    else:
        vertex_position = (a[0], c[1])

    return vertex_position


def solve(path: str, part: int) -> None:
    tiles = load_file(path)

    max_area = 1
    if part == 1:
        print("Solving for part 1")
        for i, pivot in enumerate(tiles):
            for opposite in tiles[i + 1 :]:
                area = rectangle_area(pivot, opposite)
                if area > max_area:
                    max_area = area
        print(f"Max area found: {max_area}")
    else:
        print("Solving for part 2")
        base_node = build_perimeter(tiles)
        current_node = base_node
        count = 0
        while current_node and current_node.next:
            count += 1
            # Setup for next iteration
            current_node = current_node.next
            if current_node.position == base_node.position:
                break
        print(f"Nodes: {count}")

    print(f"Max area found: {max_area}")


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
