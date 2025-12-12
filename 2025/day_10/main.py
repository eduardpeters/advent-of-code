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


def lights_equal(a: list[int], b: list[int]) -> bool:
    for light_a, light_b in zip(a, b):
        if light_a != light_b:
            return False
    return True


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
                if lights_equal(goal, new_state):
                    return presses
                new_queue.append((new_state, idx))
        queue = new_queue

    return presses


def solve(path: str, part: int) -> None:
    config_lines = load_file(path)
    machines: list[MachineConfiguration] = []
    for config in config_lines:
        machines.append(MachineConfiguration(config))

    if part == 1:
        print("Solving for part 1")
        press_count = 0
        for machine in machines:
            press_count += toggle_indicator_lights(machine.lights, machine.buttons)

        print(f"Button presses: {press_count}")
    else:
        print("Solving for part 2")


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
