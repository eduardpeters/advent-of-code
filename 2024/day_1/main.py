def solve(path: str, part: int) -> None:
    left_column, right_column = get_columns_from_file(path)
    if part == 1:
        print("Sorting and Adding Distances")
        left_column.sort()
        right_column.sort()
        total = get_total_distance(left_column, right_column)
        print(f"Total Distance: {total}")
    else:
        print("Counting and Multiplying")
        right_counts = get_id_count(right_column)
        similarity_score = get_similarity_score(left_column, right_counts)
        print(f"Similarity Score: {similarity_score}")


def get_columns_from_file(path: str) -> tuple[list[int], list[int]]:
    left_column: list[int] = []
    right_column: list[int] = []
    with open(path) as input_file:
        for line in input_file:
            columns = line.split()
            left_column.append(int(columns[0]))
            right_column.append(int(columns[1]))
    return left_column, right_column


def get_id_count(column: list[int]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for id in column:
        if id in counts:
            counts[id] += 1
        else:
            counts[id] = 1
    return counts


def get_total_distance(left_column: list[int], right_column: list[int]) -> int:
    total = 0
    for a, b in zip(left_column, right_column):
        total += a - b if a > b else b - a
    return total


def get_similarity_score(left_column: list[int], right_counts: dict[int, int]) -> int:
    similarity_score = 0
    for id in left_column:
        right_count = right_counts.get(id)
        if right_count:
            similarity_score += id * right_count
    return similarity_score


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
