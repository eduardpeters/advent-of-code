import copy
import numpy as np

ON = 1
OFF = 0


class MachineConfiguration:
    def __init__(self, config: str) -> None:
        self.lights: list[int] = []
        self.buttons: list[list[int]] = []
        self.joltage: list[int] = []

        parts = config.split()
        for part in parts:
            if part[0] == "[":
                for light in part[1:-1]:
                    parsed_light = ON if light == "#" else OFF
                    self.lights.append(parsed_light)
            elif part[0] == "(":
                new_button: list[int] = []
                for light in part[1:-1].split(","):
                    new_button.append(int(light))
                self.buttons.append(new_button)
            elif part[0] == "{":
                for joltage in part[1:-1].split(","):
                    self.joltage.append(int(joltage))


def press_button(lights: list[int], button: list[int]) -> list[int]:
    for toggle in button:
        lights[toggle] = ON if lights[toggle] == OFF else OFF
    return lights


def toggle_indicator_lights(goal: list[int], buttons: list[list[int]]) -> int:
    presses = 0
    light_state = [OFF for _ in goal]
    queue: list[tuple[list[int], int]] = [(light_state, -1) for _ in buttons]
    while queue:
        presses += 1
        new_queue: list[tuple[list[int], int]] = []
        for state, last_button_idx in queue:
            for idx, button in enumerate(buttons):
                if last_button_idx == idx:
                    continue
                new_state = press_button(state[:], button)
                if goal == new_state:
                    return presses
                new_queue.append((new_state, idx))
        queue = new_queue

    return presses


def print_matrix(matrix: list[np.ndarray], title: str = ""):
    print(title)
    for row in matrix:
        print(row)


def apply_joltage(joltage: list[int], button: list[int]) -> list[int]:
    for idx in button:
        joltage[idx] += 1
    return joltage


def has_overjoltage(goal: list[int], joltage: list[int]) -> bool:
    for goal_joltage, current_joltage in zip(goal, joltage):
        if current_joltage > goal_joltage:
            return True
    return False


def build_matrix(goal: list[int], buttons: list[list[int]]) -> list[np.ndarray]:
    equations = [np.array([0 for _ in buttons]) for _ in goal]
    for e_idx, equation in enumerate(equations):
        for b_idx, button in enumerate(buttons):
            for idx in button:
                if idx != e_idx:
                    continue
                equation[b_idx] = 1
    result = np.array(goal)
    matrix: list[np.ndarray] = []
    for equation, result in zip(equations, result):
        row = np.append(equation, result)
        matrix.append(row)

    return matrix


def matrix_elimination(matrix: list[np.ndarray]) -> list[np.ndarray]:
    for idx in range(min(len(matrix), len(matrix[0]))):
        if matrix[idx][idx] == 0:
            best_swap_row = -1
            for row in range(idx + 1, len(matrix)):
                if matrix[row][idx] != 0:
                    if matrix[row][idx] == 1:
                        best_swap_row = row
                    elif matrix[row][idx] > 0:
                        if best_swap_row < 0:
                            best_swap_row = row
                        elif matrix[row][idx] < matrix[best_swap_row][idx]:
                            best_swap_row = row
            tmp = matrix[best_swap_row]
            matrix[best_swap_row] = matrix[idx]
            matrix[idx] = tmp
        elif matrix[idx][idx] != 0:
            factor = 1 // matrix[idx][idx]
            matrix[idx] = factor * matrix[idx]
        for row in range(idx + 1, len(matrix)):
            if matrix[row][idx] != 0:
                factor = matrix[row][idx] // matrix[idx][idx]
                matrix[row] -= factor * matrix[idx]

    return matrix


def count_variables(equation: np.ndarray) -> int:
    count = 0
    for var in equation[:-1]:
        if var != 0:
            count += 1
    return count


def solve_single_variable(equation: np.ndarray) -> tuple[int, tuple[int, int]] | None:
    idx_coefficient = -1
    for coeff in equation[:-1]:
        idx_coefficient += 1
        if coeff != 0:
            break
    if equation[-1] % equation[idx_coefficient] != 0:
        return None
    result = equation[-1] // equation[idx_coefficient]
    return idx_coefficient, (result.item(), result.item())


def constrain_upper_bounds_by_equation(
    equation: np.ndarray, coefficients: list[tuple[int, int]], seen_indeces: set[int]
) -> list[tuple[int, tuple[int, int]]]:
    updated: list[tuple[int, tuple[int, int]]] = []

    equation_coefficients: list[int] = [
        idx for idx, value in enumerate(equation[:-1]) if value != 0
    ]
    idx_pivot = 0
    while idx_pivot < len(equation) - 1:
        coefficient_pivot = equation[idx_pivot]
        if coefficient_pivot == 0 or idx_pivot in seen_indeces:
            idx_pivot += 1
            continue
        pivot_upper_bound = equation[-1]
        for idx_coefficient in equation_coefficients:
            if idx_coefficient == idx_pivot:
                continue
            value_coefficient = equation[idx_coefficient]
            if value_coefficient < 0:
                coefficient_upper_bound = coefficients[idx_coefficient][1]
                coefficient_bound_factor = (
                    coefficient_upper_bound if coefficient_upper_bound != -1 else 0
                )
            else:
                coefficient_bound_factor = coefficients[idx_coefficient][0]

            pivot_upper_bound -= equation[idx_coefficient] * coefficient_bound_factor
        if pivot_upper_bound % coefficient_pivot == 0:
            pivot_upper_bound = pivot_upper_bound // coefficient_pivot
            if pivot_upper_bound >= 0:
                seen_indeces.add(idx_pivot)
                updated.append(
                    (
                        idx_pivot,
                        (coefficients[idx_pivot][0], pivot_upper_bound.item()),
                    )
                )
        idx_pivot += 1

    return updated


def constrain_lower_bounds_by_equation(
    equation: np.ndarray, coefficients: list[tuple[int, int]], seen_indeces: set[int]
) -> list[tuple[int, tuple[int, int]]]:
    updated: list[tuple[int, tuple[int, int]]] = []

    equation_coefficients: list[int] = [
        idx for idx, value in enumerate(equation[:-1]) if value != 0
    ]
    idx_pivot = 0
    while idx_pivot < len(equation) - 1:
        coefficient_pivot = equation[idx_pivot]
        if coefficient_pivot == 0 or idx_pivot in seen_indeces:
            idx_pivot += 1
            continue
        pivot_lower_bound = equation[-1]
        for idx_coefficient in equation_coefficients:
            if idx_coefficient == idx_pivot:
                continue
            value_coefficient = equation[idx_coefficient]
            if value_coefficient < 0:
                coefficient_bound_factor = coefficients[idx_coefficient][0]
            else:
                coefficient_bound_factor = coefficients[idx_coefficient][1]

            if coefficient_bound_factor < 0:
                pivot_lower_bound = -1
            else:
                pivot_lower_bound -= (
                    equation[idx_coefficient] * coefficient_bound_factor
                )

        if pivot_lower_bound >= 0 and pivot_lower_bound % coefficient_pivot == 0:
            pivot_lower_bound = pivot_lower_bound // coefficient_pivot
            if pivot_lower_bound >= 0:
                seen_indeces.add(idx_pivot)
                updated.append(
                    (
                        idx_pivot,
                        (pivot_lower_bound.item(), coefficients[idx_pivot][1]),
                    )
                )
        idx_pivot += 1

    return updated


def constrain_coefficients(
    matrix: list[np.ndarray], coefficients: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    seen: set[int] = set()
    for row in matrix[::-1]:
        variables = count_variables(row)
        if variables <= 0:
            continue
        if variables == 1:
            solved = solve_single_variable(row)
            if not solved:
                continue
            coefficients[solved[0]] = solved[1]
            seen.add(solved[0])
        else:
            coefficient_updates = constrain_upper_bounds_by_equation(
                row, coefficients, seen
            )
            for idx, bounds in coefficient_updates:
                coefficients[idx] = bounds

    seen = set()
    for row in matrix[::-1]:
        variables = count_variables(row)
        if variables <= 0:
            continue
        if variables == 1:
            for idx in range(len(row) - 1):
                if row[idx] > 0:
                    seen.add(idx)
                    break
        else:
            coefficient_updates = constrain_lower_bounds_by_equation(
                row, coefficients, seen
            )
            for idx, bounds in coefficient_updates:
                coefficients[idx] = bounds

    return coefficients


def is_valid_solution(matrix: list[np.ndarray], coefficients: list[int]) -> bool:
    for row in matrix:
        lhs = 0
        for idx, param in enumerate(row[:-1]):
            lhs += param * coefficients[idx]
        rhs = row[-1]

        if lhs != rhs:
            return False

    return True


def raise_joltage(goal: list[int], buttons: list[list[int]]) -> int:
    print(f"Solving for: {goal} using {len(buttons)} buttons")
    matrix = build_matrix(goal, buttons)
    reduced_matrix = matrix_elimination(copy.deepcopy(matrix))
    coefficients_bounds: list[tuple[int, int]] = [(0, -1) for _ in matrix[0][:-1]]
    coefficients_bounds = constrain_coefficients(reduced_matrix, coefficients_bounds)
    for idx, coef in enumerate(coefficients_bounds):
        print(f"Button {idx + 1} Bounds: {coef}")
    queue: list[tuple[int, list[int]]] = []
    lowest_presses: list[int] = []
    for idx, bounds in enumerate(coefficients_bounds):
        if bounds[1] == -1 or bounds[1] >= bounds[0]:
            presses = [b[0] for b in coefficients_bounds]
            queue.append((idx, presses))
            break

    while queue:
        print(f"Level size: {len(queue)}")
        new_queue: list[tuple[int, list[int]]] = []
        for start_idx, state in queue:
            if sum(state) >= min(goal) and is_valid_solution(matrix, state):
                if not lowest_presses or sum(state) < sum(lowest_presses):
                    print(f"Found new lowest: {state}")
                    lowest_presses = state

            state_coefficients_bounds = constrain_coefficients(
                reduced_matrix,
                [
                    (value, bounds[1]) if value < bounds[1] else (bounds[1], bounds[1])
                    for value, bounds in zip(state, coefficients_bounds)
                ],
            )
            for idx, bounds in enumerate(state_coefficients_bounds):
                if idx < start_idx:
                    continue
                if bounds[1] == -1 or bounds[1] > state[idx]:
                    new_state = state[:]
                    new_state[idx] += 1
                    if lowest_presses and sum(new_state) >= sum(lowest_presses):
                        continue
                    new_queue.append((idx, new_state))

        queue = new_queue

    print(f"Min presses found for {goal}: {sum(lowest_presses)}")
    return sum(lowest_presses)


def solve(path: str, part: int) -> None:
    config_lines = load_file(path)
    machines: list[MachineConfiguration] = []
    for config in config_lines:
        machines.append(MachineConfiguration(config))

    press_count = 0
    if part == 1:
        print("Solving for part 1")
        for machine in machines:
            press_count += toggle_indicator_lights(machine.lights, machine.buttons)

    else:
        print("Solving for part 2")
        machines.sort(key=lambda m: len(m.buttons))
        for machine in machines:
            press_count += raise_joltage(machine.joltage, machine.buttons)

    print(f"Button presses: {press_count}")


def load_file(path: str) -> list[str]:
    lines: list[str] = []

    with open(path) as file:
        for line in file:
            lines.append(line)

    return lines


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
