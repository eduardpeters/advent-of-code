def solve(path: str, part: int) -> None:
    rules, updates = load_file(path)
    print(rules)
    correct_updates, incorrect_updates = get_classified_updates(rules, updates)
    if part == 1:
        print("Solving for part 1")
        print(f"Correct updates: {correct_updates}")
        middle_page_sum = get_middle_page_sum(correct_updates)
    else:
        print("Solving for part 2")
        print(f"Incorrect updates:")
        print(incorrect_updates)
        corrected_updates = amend_incorrect_updates(rules, incorrect_updates)
        print("Corrected updates")
        print(corrected_updates)
        middle_page_sum = get_middle_page_sum(corrected_updates)
    print(f"Middle page sum: {middle_page_sum}")


def get_middle_page_sum(updates: list[list[int]]) -> int:
    return sum([update[len(update) // 2] for update in updates])


def get_classified_updates(
    rules: dict[int, list[int]], updates: list[list[int]]
) -> tuple[list[list[int]], list[list[int]]]:
    correct_updates: list[list[int]] = []
    incorrect_updates: list[list[int]] = []
    for update in updates:
        for i in range(1, len(update)):
            current_page = update[i]
            if current_page not in rules:
                continue
            for j in range(i - 1, -1, -1):
                preceding_page = update[j]
                if preceding_page in rules[current_page]:
                    incorrect_updates.append(update)
                    break
            else:
                continue  # for loop found no invalid numbers, check next number
            break  # found invalid page positions, break out
        else:
            # only if inner loop did not break is the update valid
            correct_updates.append(update)

    return correct_updates, incorrect_updates


def amend_incorrect_updates(
    rules: dict[int, list[int]], incorrect_updates: list[list[int]]
) -> list[list[int]]:
    corrected_updates: list[list[int]] = []
    for incorrect_update in incorrect_updates:
        corrected_update: list[int] = incorrect_update
        i: int = 1
        while i < len(corrected_update):
            current_page = corrected_update[i]
            if current_page not in rules:
                i += 1
                continue
            j: int = i - 1
            while j > -1:
                preceding_page = corrected_update[j]
                if preceding_page in rules[current_page]:
                    page_to_move = corrected_update.pop(j)
                    corrected_update.append(page_to_move)
                    # Update current page index to account for list shift
                    i -= 1
                j -= 1
            i += 1
        corrected_updates.append(corrected_update)

    return corrected_updates


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
