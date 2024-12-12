EMPTY_BLOCK = "."


def solve(path: str, part: int) -> None:
    disk_map = load_file(path)
    print(len(disk_map))
    expanded = expand_disk_map(disk_map)
    print(len(expanded))
    if part == 1:
        print("Solving for part 1")
        fragmented = fragment_disk(expanded)
        checksum = calculate_checksum(fragmented)
        print(f"Disk checksum is {checksum}")
    else:
        print("Solving for part 2")


def expand_disk_map(disk_map: str) -> list[int | str]:
    expanded_disk: list[int | str] = []

    is_file = True
    file_id = 0
    for value in disk_map:
        block_size = int(value)
        new_blocks = [file_id if is_file else EMPTY_BLOCK for _ in range(block_size)]
        expanded_disk.extend(new_blocks)

        if is_file:
            file_id += 1
        is_file = not is_file

    return expanded_disk


def fragment_disk(expanded_disk: list[int | str]) -> list[int | str]:
    head_pointer: int = 0
    tail_pointer: int = len(expanded_disk) - 1

    while head_pointer < tail_pointer:
        # Move head_pointer to next empty position
        while expanded_disk[head_pointer] != EMPTY_BLOCK:
            head_pointer += 1
        # Move tail_pointer to next non-empty position
        while expanded_disk[tail_pointer] == EMPTY_BLOCK:
            tail_pointer -= 1
        if tail_pointer <= head_pointer:
            break

        expanded_disk[head_pointer] = expanded_disk[tail_pointer]
        expanded_disk[tail_pointer] = EMPTY_BLOCK
        head_pointer += 1
        tail_pointer -= 1

    return expanded_disk


def calculate_checksum(disk: list[int | str]) -> int:
    checksum = 0
    position = 0
    for block in disk:
        if not isinstance(block, int):
            break
        checksum += position * block
        position += 1
    return checksum


def load_file(path: str) -> str:
    with open(path) as file:
        return file.readline()


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
