STARTING_NODE = "you"
GOAL_NODE = "out"


def paths_to_goal(map: dict[str, list[str]], visited: set[str], current: str) -> int:
    if current in visited:
        return 0
    if current == GOAL_NODE:
        return 1
    visited.add(current)
    connections = map[current]
    paths = 0
    for conn in connections:
        new_visited = visited.copy()
        paths += paths_to_goal(map, new_visited, conn)
    return paths


def solve(path: str, part: int) -> None:
    node_map = load_file(path)

    # print(node_map)

    if part == 1:
        print("Solving for part 1")
        paths = paths_to_goal(node_map, set(), STARTING_NODE)
        print(f"Paths: {paths}")
    else:
        print("Solving for part 2")


def load_file(path: str) -> dict[str, list[str]]:
    map: dict[str, list[str]] = {}

    with open(path) as file:
        for line in file:
            name, connections = line.strip().split(": ")
            name_connections: list[str] = []
            for conn in connections.strip().split():
                name_connections.append(conn)
            map[name] = name_connections

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
