def solve(path: str, part: int) -> None:
    rules, updates = load_file(path)
    print(rules)
    print(updates)
    if part == 1:
        print("Solving for part 1")
        correct_updates = get_correct_updates(rules, updates)
        print(f"Correct updates: {correct_updates}")
        middle_page_sum = sum([update[len(update) // 2] for update in correct_updates])
        print(f"Middle page sum: {middle_page_sum}")
    else:
        print("Solving for part 2")


def get_correct_updates(
    rules: dict[int, list[int]], updates: list[list[int]]
) -> list[list[int]]:
    correct_updates: list[list[int]] = []
    for update in updates:
        for i in range(1, len(update)):
            current_page = update[i]
            if current_page not in rules:
                continue
            for j in range(i - 1, -1, -1):
                preceding_page = update[j]
                if preceding_page in rules[current_page]:
                    break
            else:
                continue  # for loop found no invalid numbers, check next number
            break  # found invalid page positions, break out
        else:
            # only if inner loop did not break is the update valid
            correct_updates.append(update)

    return correct_updates


def load_file(path: str):
    rules: dict[int, list[int]] = {}
    updates: list[list[int]] = []

    is_update: bool = False
    with open(path) as file:
        for line in file:
            trimmed_line = line.strip()
            if not trimmed_line:
                is_update = True
                continue
            if is_update:
                updates.append([int(number) for number in trimmed_line.split(",")])
            else:
                first_page, second_page = [
                    int(number) for number in trimmed_line.split("|")
                ]
                if first_page in rules:
                    rules[first_page].append(second_page)
                else:
                    rules[first_page] = [second_page]
    return rules, updates


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
