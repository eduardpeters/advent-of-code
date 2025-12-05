def overlaps(a: tuple[int, int], b: tuple[int, int]) -> bool:
    if a[1] < b[0]:
        return False
    if b[1] < a[0]:
        return False
    return True


def merge(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    if a[0] <= b[0]:
        lower = a[0]
    else:
        lower = b[0]

    if a[1] >= b[1]:
        higher = a[1]
    else:
        higher = b[1]

    return (lower, higher)


def is_contained(range: tuple[int, int], value: int) -> bool:
    return value >= range[0] and value <= range[1]


def merge_fresh_ranges(fresh_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    has_merged = False
    merged_ranges: list[tuple[int, int]] = [fresh_ranges[0]]

    for fresh_range in fresh_ranges[1:]:
        for i in range(len(merged_ranges)):
            if overlaps(fresh_range, merged_ranges[i]):
                merged_ranges[i] = merge(fresh_range, merged_ranges[i])
                has_merged = True
                break
        else:
            merged_ranges.append(fresh_range)

    return merge_fresh_ranges(merged_ranges) if has_merged else merged_ranges


def solve(path: str, part: int) -> None:
    fresh_ranges, available_ingredients = load_file(path)
    print("fresh", len(fresh_ranges))
    print("available", len(available_ingredients))

    fresh_ranges = merge_fresh_ranges(fresh_ranges)
    print("merged", len(fresh_ranges))

    if part == 1:
        print("Solving for part 1")
        fresh_ranges.sort(key=lambda fr: fr[0])
        fresh_available_count = 0
        for ingredient in available_ingredients:
            if ingredient < fresh_ranges[0][0] or ingredient > fresh_ranges[-1][1]:
                continue

            for fresh_range in fresh_ranges:
                if is_contained(fresh_range, ingredient):
                    fresh_available_count += 1
                    break

        print(f"Fresh and available count: {fresh_available_count}")

    else:
        print("Solving for part 2")
        fresh_possible_count = 0
        for fresh_range in fresh_ranges:
            fresh_possible_count += fresh_range[1] - fresh_range[0] + 1

        print(f"Fresh ingredient IDs: {fresh_possible_count}")


def load_file(path: str) -> tuple[list[tuple[int, int]], list[int]]:
    fresh_ranges: list[tuple[int, int]] = []
    available_ingredients: list[int] = []

    ranges_flag = True
    with open(path) as file:
        for line in file:
            current_line = line.strip()
            if not current_line:
                ranges_flag = False
                continue
            if ranges_flag:
                start, end = current_line.split("-")
                fresh_ranges.append((int(start), int(end)))
            else:
                available_ingredients.append(int(current_line))

    return fresh_ranges, available_ingredients


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
