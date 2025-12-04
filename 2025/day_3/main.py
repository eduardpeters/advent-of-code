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


def solve(path: str, part: int) -> None:
    banks = load_file(path)

    if part == 1:
        joltage = 0
        print("Solving for part 1")
        for bank in banks:
            joltage += get_bank_joltage_pair(bank)
        print(f"Joltage: {joltage}")
    else:
        print("Solving for part 2")


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
