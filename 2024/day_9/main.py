EMPTY_BLOCK = "."


def solve(path: str, part: int) -> None:
    disk_map = load_file(path)
    expanded, file_sizes = expand_disk_map(disk_map)
    if part == 1:
        print("Solving for part 1")
        fragmented = fragment_disk(expanded)
        checksum = calculate_checksum(fragmented)
    else:
        print("Solving for part 2")
        defragmented = defragment_disk(expanded, file_sizes)
        # print(defragmented)
        checksum = calculate_checksum(defragmented)
    print(f"Disk checksum is {checksum}")


def expand_disk_map(disk_map: str) -> tuple[list[int | str], dict[int, int]]:
    expanded_disk: list[int | str] = []
    file_sizes: dict[int, int] = {}

    is_file = True
    file_id = 0
    for value in disk_map:
        block_size = int(value)
        new_blocks = [file_id if is_file else EMPTY_BLOCK for _ in range(block_size)]
        expanded_disk.extend(new_blocks)

        if is_file:
            file_sizes[file_id] = block_size
            file_id += 1
        is_file = not is_file

    return expanded_disk, file_sizes


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


def defragment_disk(
    expanded_disk: list[int | str], file_sizes: dict[int, int]
) -> list[int | str]:
    descending_ids = sorted(file_sizes.keys(), reverse=True)

    for id in descending_ids:
        print(f"Checking File ID: {id}")
        next_file_bounds = get_file_bounds(expanded_disk, id)
        if not next_file_bounds:
            raise ValueError("File ID not found in disk")
        file_size = file_sizes[id]
        next_empty_blocks = find_next_empty_blocks(expanded_disk, 0)
        if not next_empty_blocks:
            # No more empty blocks
            return expanded_disk
        while next_empty_blocks[1] - next_empty_blocks[0] < file_size:
            if next_empty_blocks[1] > next_file_bounds[0]:
                break
            next_empty_blocks = find_next_empty_blocks(
                expanded_disk, next_empty_blocks[1]
            )
            if not next_empty_blocks:
                break

        if (
            next_empty_blocks
            and next_empty_blocks[0] < next_file_bounds[0]
            and next_empty_blocks[1] - next_empty_blocks[0] >= file_size
        ):
            for i in range(next_file_bounds[1] - next_file_bounds[0]):
                expanded_disk[next_empty_blocks[0] + i] = id
                expanded_disk[next_file_bounds[0] + i] = EMPTY_BLOCK

    return expanded_disk


def get_file_bounds(disk: list[int | str], id: int) -> tuple[int, int] | None:
    file_bounds: tuple[int, int] = (-1, -1)
    for i, block in enumerate(disk):
        if block == id:
            if file_bounds[0] == -1:
                file_bounds = (i, -1)
        else:
            if file_bounds[0] != -1:
                file_bounds = (file_bounds[0], i)
                break
            else:
                continue
    if file_bounds == (-1, -1):
        return None
    elif file_bounds[1] == -1:
        return file_bounds[0], len(disk)
    return file_bounds


def find_next_empty_blocks(
    disk: list[int | str], starting_position: int
) -> tuple[int, int] | None:
    empty_blocks_bounds: tuple[int, int] = (-1, -1)
    for i in range(starting_position, len(disk)):
        current_block = disk[i]
        if current_block == EMPTY_BLOCK:
            if empty_blocks_bounds[0] == -1:
                empty_blocks_bounds = (i, -1)
        else:
            if empty_blocks_bounds[0] != -1:
                empty_blocks_bounds = (empty_blocks_bounds[0], i)
                break
    if empty_blocks_bounds == (-1, -1):
        return None
    elif empty_blocks_bounds[1] == -1:
        return empty_blocks_bounds[0], len(disk)
    else:
        return empty_blocks_bounds


def calculate_checksum(disk: list[int | str], is_defragmented: bool = False) -> int:
    checksum = 0
    position = 0
    for block in disk:
        if not isinstance(block, int):
            if is_defragmented:
                break
            else:
                position += 1
                continue
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
