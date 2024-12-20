INCREASING = 1
DECREASING = -1


def solve(path: str, part: int) -> None:
    print("Getting levels")
    reports = get_reports(path)
    reports = parse_reports(reports)

    using_damper = part != 1
    if using_damper:
        print("Solving with Problem Damper")
    else:
        print("Solving without removal")

    safe_count: int = 0

    for report in reports:
        if is_report_safe(report, part != 1):
            safe_count += 1
        else:
            print(f"Unsafe: {report}")

    print(f"Safe Reports: {safe_count}")


def get_reports(path: str) -> list[str]:
    reports: list[str] = [line.strip() for line in open(path)]
    return reports


def parse_reports(reports: list[str]) -> list[list[int]]:
    parsed_reports = [report_to_levels(report) for report in reports]
    return parsed_reports


def report_to_levels(report: str) -> list[int]:
    levels = [int(level) for level in report.split()]
    return levels


def is_report_safe(report: list[int], with_damper: bool = False) -> bool:
    report_trend = get_trend(report[0], report[1])
    for i in range(1, len(report)):
        a, b = report[i - 1], report[i]
        if i != 1:
            trend = get_trend(a, b)
            if trend != report_trend:
                if not with_damper:
                    return False
                return is_damped_report_safe(report, i)
        diff = get_difference(a, b)
        if diff < 1 or 3 < diff:
            if not with_damper:
                return False
            return is_damped_report_safe(report, i)
    return True


def is_damped_report_safe(report: list[int], current_index: int) -> bool:
    damped_report = report[:current_index] + report[current_index + 1 :]
    if is_report_safe(damped_report):
        return True
    damped_report = report[: current_index - 1] + report[current_index:]
    if is_report_safe(damped_report):
        return True
    damped_report = report[1:]
    return is_report_safe(damped_report)


def get_trend(a: int, b: int) -> int:
    return INCREASING if a < b else DECREASING


def get_difference(a: int, b: int) -> int:
    return a - b if a > b else b - a


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
