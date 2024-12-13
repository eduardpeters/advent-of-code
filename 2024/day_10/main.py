LOWEST_HEIGHT = 0
HIGHEST_HEIGHT = 9


def solve(path: str, part: int) -> None:
    map = load_file(path)
    if part == 1:
        print("Solving for part 1")
        trailheads_score = count_trailheads(map)
        print(f"Trailhead total score {trailheads_score}")
    else:
        print("Solving for part 2")
        trailheads_rating = count_trailheads(map, use_rating=True)
        print(f"Trailhead total rating {trailheads_rating}")


def count_trailheads(map: list[list[int]], use_rating: bool = False) -> int:
    total_score: int = 0
    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            current_height = map[y][x]
            if current_height == LOWEST_HEIGHT:
                score: int = 0
                visited: set[tuple[int, int]] | None = None if use_rating else set()
                # Check above
                direction_score, visited = traverse_trailhead(
                    map, y - 1, x, LOWEST_HEIGHT + 1, visited
                )
                score += direction_score
                # Check forward
                direction_score, visited = traverse_trailhead(
                    map, y, x + 1, LOWEST_HEIGHT + 1, visited
                )
                score += direction_score
                # Check below
                direction_score, visited = traverse_trailhead(
                    map, y + 1, x, LOWEST_HEIGHT + 1, visited
                )
                score += direction_score
                # Check behind
                direction_score, visited = traverse_trailhead(
                    map, y, x - 1, LOWEST_HEIGHT + 1, visited
                )
                score += direction_score
                total_score += score
    return total_score


def traverse_trailhead(
    map: list[list[int]],
    current_y: int,
    current_x: int,
    next_height: int,
    visited: set[tuple[int, int]] | None,
) -> tuple[int, set[tuple[int, int]] | None]:
    if current_y < 0 or len(map) <= current_y:
        return 0, visited
    if current_x < 0 or len(map[current_y]) <= current_x:
        return 0, visited

    current_height = map[current_y][current_x]
    if current_height != next_height:
        return 0, visited

    if current_height == HIGHEST_HEIGHT:
        if visited is not None:
            current_position = (current_y, current_x)
            if current_position in visited:
                return 0, visited
            else:
                visited.add(current_position)
        return 1, visited

    count: int = 0
    direction_count, visited = traverse_trailhead(
        map, current_y - 1, current_x, next_height + 1, visited
    )
    count += direction_count
    direction_count, visited = traverse_trailhead(
        map, current_y, current_x + 1, next_height + 1, visited
    )
    count += direction_count
    direction_count, visited = traverse_trailhead(
        map, current_y + 1, current_x, next_height + 1, visited
    )
    count += direction_count
    direction_count, visited = traverse_trailhead(
        map, current_y, current_x - 1, next_height + 1, visited
    )
    count += direction_count
    return count, visited


def load_file(path: str) -> list[list[int]]:
    map: list[list[int]] = []
    with open(path) as file:
        for line in file:
            row = [int(height) if height != "." else -1 for height in line.strip()]
            map.append(row)
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
