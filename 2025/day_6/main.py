ADD = "+"
MULTIPLY = "*"


def load_raw_file_reversed(path: str) -> list[str]:
    lines: list[str] = []
    with open(path) as file:
        for line in file:
            lines.append(line.removesuffix("\n")[::-1])
    return lines


def solve(path: str, part: int) -> None:
    if part == 1:
        print("Solving for part 1")
        numbers, operators = load_file(path)
        grand_total = 0
        problem = 0
        while problem < len(numbers):
            op = operators[problem]
            result = 0 if op == ADD else 1
            for number in numbers[problem]:
                if op == ADD:
                    result += number
                else:
                    result *= number

            grand_total += result
            problem += 1

        print(f"Grand Total: {grand_total}")
    else:
        print("Solving for part 2")
        lines = load_raw_file_reversed(path)
        numbers: list[list[int]] = []
        operators: list[str] = []
        # Initialize an array for each possible problem set
        for _ in range(len(lines[0].split())):
            numbers.append([])
        # Extract operators
        for op in lines[-1].strip().split():
            operators.append(op)
        problem_idx = 0
        n_columns = len(lines[0])
        for c in range(n_columns):
            column_has_number = False
            current_number = 0
            for line in lines[:-1]:
                current_char = line[c]
                if current_char == " ":
                    continue
                column_has_number = True
                current_number = current_number * 10 + int(current_char)
            if column_has_number:
                numbers[problem_idx].append(current_number)
            else:
                problem_idx += 1
        grand_total = 0
        problem_idx = 0
        while problem_idx < len(numbers):
            op = operators[problem_idx]
            result = 0 if op == ADD else 1
            for number in numbers[problem_idx]:
                if op == ADD:
                    result += number
                else:
                    result *= number

            grand_total += result
            problem_idx += 1

        print(f"Grand Total: {grand_total}")


def load_file(path: str) -> tuple[list[list[int]], list[str]]:
    numbers: list[list[int]] = []
    operators: list[str] = []

    with open(path) as file:
        for line in file:
            current_line = line.strip().split()
            if not numbers:
                for _ in range(len(current_line)):
                    numbers.append([])
            if current_line[0] == ADD or current_line[0] == MULTIPLY:
                for op in current_line:
                    operators.append(op)
            else:
                i = 0
                while i < len(current_line):
                    numbers[i].append(int(current_line[i]))
                    i += 1

    return numbers, operators


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
