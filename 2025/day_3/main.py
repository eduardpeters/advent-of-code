def get_bank_joltage_pair(bank: str) -> int:
    batteries = [int(b) for b in bank]
    high_h_idx = 0
    high_l_idx = 1
    i = 1
    while i < len(batteries) - 1:
        if batteries[i] > batteries[high_h_idx]:
            high_h_idx = i
            high_l_idx = i + 1
        elif batteries[i] > batteries[high_l_idx]:
            high_l_idx = i
        i += 1
    if batteries[i] > batteries[high_l_idx]:
        high_l_idx = i

    return int(bank[high_h_idx] + bank[high_l_idx])


def get_bank_joltage_dozen(bank: str) -> int:
    batteries = [int(b) for b in bank]
    indexes: list[int] = [i for i in range(12)]

    current_index = 0
    while current_index < len(indexes):
        i = indexes[current_index] + 1
        while i < (len(batteries) - len(indexes) + current_index + 1):
            if batteries[i] > batteries[indexes[current_index]]:
                for idx in range(len(indexes[current_index:])):
                    indexes[current_index + idx] = i + idx
            i += 1

        # Exit early if all remaining batteries needed complete dozen
        if indexes[current_index] >= len(batteries) - len(indexes) + current_index:
            break

        current_index += 1

    return int("".join([str(batteries[idx]) for idx in indexes]))


def solve(path: str, part: int) -> None:
    banks = load_file(path)

    joltage = 0
    if part == 1:
        print("Solving for part 1")
        for bank in banks:
            joltage += get_bank_joltage_pair(bank)
    else:
        print("Solving for part 2")
        for bank in banks:
            joltage += get_bank_joltage_dozen(bank)

    print(f"Joltage: {joltage}")


def load_file(path: str) -> list[str]:
    banks: list[str] = []
    with open(path) as file:
        for line in file:
            banks.append(line.strip())
    return banks


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
