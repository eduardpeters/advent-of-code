from dataclasses import dataclass
from math import sqrt
from typing import Any


@dataclass
class BoxNode:
    position: tuple[int, int, int]
    connections: list["BoxNode"]

    def size(self) -> int:
        size = 1
        for connection in self.connections:
            size += connection.size()
        return size


def build_node(
    visited: set[tuple[int, int, int]],
    pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]],
    base: tuple[int, int, int],
) -> BoxNode | None:
    # If box has been visited, it is already in a circuit
    if base in visited:
        return None
    # We register we have added this box
    visited.add(base)
    node = BoxNode(position=base, connections=[])
    # We look for all connections to base box
    for pair in pairs:
        if pair[0] != base and pair[1] != base:
            continue
        if pair[0] == base:
            connection_node = build_node(visited, pairs, pair[1])
        else:
            connection_node = build_node(visited, pairs, pair[0])
        if connection_node:
            node.connections.append(connection_node)

    return node


def build_graphs(
    pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]],
) -> list[BoxNode]:
    visited: set[tuple[int, int, int]] = set()

    graphs: list[BoxNode] = []
    for i in range(len(pairs)):
        node = build_node(visited, pairs, pairs[i][0])
        if node:
            graphs.append(node)

    return graphs


def get_shortest_connections(
    boxes: list[tuple[int, int, int]], n_connections: int
) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    pairs_to_connect: list[dict[str, Any]] = []
    for i, box in enumerate(boxes):
        for pair in boxes[i + 1 :]:
            pair_distance = distance(box, pair)
            entry: dict[str, Any] = {
                "distance": pair_distance,
                "box_1": box,
                "box_2": pair,
            }
            pairs_to_connect.append(entry)
    pairs_to_connect.sort(key=lambda p: p["distance"])

    shortest_pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
    for n in range(n_connections):
        pair_data = pairs_to_connect[n]
        shortest_pairs.append((pair_data["box_1"], pair_data["box_2"]))

    return shortest_pairs


def distance(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> float:
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


def solve(path: str, part: int) -> None:
    boxes = load_file(path)

    if part == 1:
        print("Solving for part 1")
        pairs_to_connect = get_shortest_connections(boxes, 1000)
        print(f"Pairs: {len(pairs_to_connect)}")
        circuits = build_graphs(pairs_to_connect)
        print(f"Circuits: {len(circuits)}")
        circuit_sizes: list[int] = [0, 0, 0]
        for circuit in circuits:
            current_size = circuit.size()
            if current_size > circuit_sizes[0]:
                circuit_sizes[2] = circuit_sizes[1]
                circuit_sizes[1] = circuit_sizes[0]
                circuit_sizes[0] = current_size
            elif current_size > circuit_sizes[1]:
                circuit_sizes[2] = circuit_sizes[1]
                circuit_sizes[1] = current_size
            elif current_size > circuit_sizes[2]:
                circuit_sizes[2] = current_size
        print(f"Three largest circuits: {circuit_sizes}")
        print(
            f"Their product: {circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]}"
        )
    else:
        print("Solving for part 2")


def load_file(path: str) -> list[tuple[int, int, int]]:
    boxes: list[tuple[int, int, int]] = []

    with open(path) as file:
        for line in file:
            x, y, z = [int(c) for c in line.strip().split(",")]
            boxes.append((x, y, z))

    return boxes


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
