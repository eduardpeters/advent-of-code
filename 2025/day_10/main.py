from functools import cache
from itertools import combinations

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


def patterns(coeffs: list[tuple[int, ...]]) -> dict[tuple[int, ...], int]:
    out: dict[tuple[int, ...], int] = {}
    num_buttons = len(coeffs)
    num_variables = len(coeffs[0])
    for pattern_len in range(num_buttons + 1):
        for buttons in combinations(range(num_buttons), pattern_len):
            pattern = tuple(
                map(sum, zip((0,) * num_variables, *(coeffs[i] for i in buttons)))
            )
            if pattern not in out:
                out[pattern] = pattern_len
    return out


def raise_joltage(goal: tuple[int, ...], buttons: list[tuple[int, ...]]) -> int:
    pattern_costs = patterns(buttons)

    @cache
    def solve_joltage(goal: tuple[int, ...]) -> int:
        if all(i == 0 for i in goal):
            return 0
        answer = 1000000
        for pattern, pattern_cost in pattern_costs.items():
            if all(i <= j and i % 2 == j % 2 for i, j in zip(pattern, goal)):
                new_goal = tuple((j - i) // 2 for i, j in zip(pattern, goal))
                answer = min(answer, pattern_cost + 2 * solve_joltage(new_goal))
        return answer

    return solve_joltage(goal)


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
        for machine in machines:
            machine_joltage = tuple(machine.joltage)
            machine_buttons = [
                tuple(int(i in button) for i in range(len(machine.joltage)))
                for button in machine.buttons
            ]
            presses = raise_joltage(machine_joltage, machine_buttons)
            print(f"Joltage: {machine_joltage} reached with {presses} presses")
            press_count += presses

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
