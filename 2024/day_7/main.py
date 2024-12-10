from dataclasses import dataclass, field
from enum import Enum


class Operation(Enum):
    SUM = 0
    MULTIPLY = 1


@dataclass
class Equation(object):
    result: int
    operands: list[int]
    operators: list[Operation] = field(default_factory=list)

    def apply_operations(self) -> int:
        # print(f"Testing {self.operands} with {self.operators}")
        result = self.operands[0]
        i = 1
        for operator in self.operators:
            next_operand = self.operands[i]
            if operator == Operation.SUM:
                result += next_operand
            else:
                result *= next_operand
            i += 1
        # print(f"Result: {result}")
        return result


def solve(path: str, part: int) -> None:
    equations = load_file(path)
    # print(equations)
    if part == 1:
        print("Solving for part 1")
        print(f"Iterating over {len(equations)} equations...")
        total = 0
        for equation in equations:
            # print(f"Testing: {equation}")
            if is_valid_equation(equation):
                total += equation.result
        print(f"Total: {total}")
    else:
        print("Solving for part 2")


def is_valid_equation(equation: Equation) -> bool:
    if len(equation.operators) >= len(equation.operands):
        return False
    if len(equation.operators) == len(equation.operands) - 1:
        result = equation.apply_operations()
        return result == equation.result

    operators_copy = [operator for operator in equation.operators]
    equation.operators.append(Operation.SUM)
    if is_valid_equation(equation):
        return True

    equation.operators = [*operators_copy, Operation.MULTIPLY]
    return is_valid_equation(equation)


def load_file(path: str) -> list[Equation]:
    equations: list[Equation] = []

    with open(path) as file:
        for line in file:
            split_line = line.strip().split(":")
            result = int(split_line[0])
            split_operands = split_line[1].strip().split(" ")
            operands = [int(operand) for operand in split_operands]
            equations.append(Equation(result=result, operands=operands))
    return equations


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
