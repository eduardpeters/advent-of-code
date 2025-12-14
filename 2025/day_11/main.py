YOU_NODE = "you"
SVR_NODE = "svr"
DAC_NODE = "dac"
FFT_NODE = "fft"
OUT_NODE = "out"


def paths_to_goal(
    goal: str,
    map: dict[str, list[str]],
    known_paths: dict[str, int],
    current: str,
) -> int:
    if current == goal:
        return 1
    if current in known_paths:
        if known_paths[current] == -1:
            # We have entered a loop, cannot reach goal
            return 0
        return known_paths[current]

    connections = map.get(current, [])
    paths = 0
    # Register we have traversed the node, even if unclear if any paths lead to goal
    known_paths[current] = -1
    for conn in connections:
        conn_paths = paths_to_goal(goal, map, known_paths, conn)
        paths += conn_paths
        known_paths[conn] = conn_paths
    known_paths[current] = paths

    return paths


def paths_to_goal_through_midpoints(
    goal: str,
    midpoints: list[str],
    map: dict[str, list[str]],
    known_paths: dict[tuple[str, str], int],
    current: str,
) -> int:
    if current == goal:
        if not midpoints:
            return 1
        return 0
    if (current, str(midpoints)) in known_paths:
        return known_paths[(current, str(midpoints))]

    connections = map.get(current, [])
    paths = 0
    # Update pending midpoints to traverse
    next_midpoints = midpoints
    if next_midpoints:
        # If we have reached the next midpoint, elminate from list
        if current == next_midpoints[0]:
            if len(next_midpoints) >= 1:
                next_midpoints = midpoints[1:]
            else:
                next_midpoints = []

    for conn in connections:
        conn_paths = paths_to_goal_through_midpoints(
            goal, next_midpoints, map, known_paths, conn
        )
        paths += conn_paths
        known_paths[(conn, str(next_midpoints))] = conn_paths
    known_paths[(current, str(midpoints))] = paths

    return paths


def solve(path: str, part: int) -> None:
    node_map = load_file(path)

    if part == 1:
        print("Solving for part 1")
        paths = paths_to_goal(OUT_NODE, node_map, {}, YOU_NODE)
        print(f"Paths: {paths}")
    else:
        print("Solving for part 2")
        paths = 0

        paths_from_fft_to_dac = paths_to_goal(DAC_NODE, node_map, {}, FFT_NODE)
        print(f"Paths from FFT to DAC: {paths_from_fft_to_dac}")
        paths_from_dac_to_fft = paths_to_goal(FFT_NODE, node_map, {}, DAC_NODE)
        print(f"Paths from DAC to FFT: {paths_from_dac_to_fft}")

        if paths_from_fft_to_dac > 0:
            print("Path is through FFT and DAC")
            paths = paths_to_goal_through_midpoints(
                OUT_NODE, [FFT_NODE, DAC_NODE], node_map, {}, SVR_NODE
            )
        else:
            print("Path is through DAC and FFT")
            paths = paths_to_goal_through_midpoints(
                OUT_NODE, [DAC_NODE, FFT_NODE], node_map, {}, SVR_NODE
            )

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
