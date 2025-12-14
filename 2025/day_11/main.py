YOU_NODE = "you"
SVR_NODE = "svr"
DAC_NODE = "dac"
FFT_NODE = "fft"
OUT_NODE = "out"


def paths_to_goal(
    goal: str,
    map: dict[str, list[str]],
    visited: set[str],
    known_paths: dict[str, int],
    current: str,
) -> int:
    print(f"Current: {current}")
    print(f"Visited? {current in visited}")
    print(f"Known path? {known_paths.get(current)}")
    if current == goal:
        return 1
    if current in known_paths:
        return known_paths[current]
    if current in visited:
        return 0
    visited.add(current)
    connections = map[current]
    paths = 0
    for conn in connections:
        new_visited = visited.copy()
        conn_paths = paths_to_goal(goal, map, new_visited, known_paths, conn)
        paths += conn_paths
        known_paths[conn] = conn_paths
    known_paths[current] = paths
    return paths


def paths_to_goal_through_midpoint(
    goal: str,
    midpoint: str,
    map: dict[str, list[str]],
    visited: set[str],
    current: str,
) -> int:
    print(current, len(visited))
    if current in visited:
        return 0
    if current == goal:
        if midpoint in visited:
            return 1
        return 0
    visited.add(current)
    connections = map[current]
    paths = 0
    for conn in connections:
        new_visited = visited.copy()
        conn_paths = paths_to_goal_through_midpoint(
            goal, midpoint, map, new_visited, conn
        )
        paths += conn_paths
    return paths


def solve(path: str, part: int) -> None:
    node_map = load_file(path)

    # print(node_map)

    if part == 1:
        print("Solving for part 1")
        paths = paths_to_goal(OUT_NODE, node_map, set(), {}, YOU_NODE)
        print(f"Paths: {paths}")
    else:
        print("Solving for part 2")
        paths = 0
        paths_from_svr_to_fft = paths_to_goal(
            FFT_NODE, node_map, {DAC_NODE}, {DAC_NODE: 0}, SVR_NODE
        )
        print(f"Paths from SVR to FFT, no DAC: {paths_from_svr_to_fft}")
        paths_from_fft_with_dac = paths_to_goal_through_midpoint(
            OUT_NODE, DAC_NODE, node_map, set(), FFT_NODE
        )
        print(f"Paths from FFT through DAC to OUT: {paths_from_fft_with_dac}")

    print(f"Paths: {paths}")


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
        solve("example_2.txt", 2)
    else:
        print("Running input part 2")
        solve("input.txt", 2)


if __name__ == "__main__":
    choose_action()
