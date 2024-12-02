INCREASING = 1
DECREASING = -1


def solve(path: str, part: int) -> None:
    print("Getting levels")
    reports = get_reports(path)
    reports = parse_reports(reports)
    safe_count: int = 0
    if part == 1:
        print("Solving without removal")
        for report in reports:
            if is_report_safe(report):
                safe_count += 1
        print(f"Safe Reports: {safe_count}")
    else:
        print("Solving with Problem Damper")
        for report in reports:
            if is_report_safe_with_damper(report):
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


def is_report_safe(report: list[int]) -> bool:
    print(report)
    report_trend = get_trend(report[0], report[1])
    for i in range(1, len(report)):
        if i != 1:
            trend = get_trend(report[i - 1], report[i])
            if trend != report_trend:
                return False
        diff = get_difference(report[i - 1], report[i])
        if diff < 1 or 3 < diff:
            return False
    return True


def is_report_safe_with_damper(report: list[int]) -> bool:
    report_trend = get_trend(report[0], report[1])
    for i in range(1, len(report)):
        if i != 1:
            trend = get_trend(report[i - 1], report[i])
            if trend != report_trend:
                damped_report = report[:i] + report[i + 1 :]
                if is_report_safe(damped_report):
                    return True
                damped_report = report[: i - 1] + report[i:]
                return is_report_safe(damped_report)
        diff = get_difference(report[i - 1], report[i])
        if diff < 1 or 3 < diff:
            damped_report = report[:i] + report[i + 1 :]
            if is_report_safe(damped_report):
                return True
            damped_report = report[: i - 1] + report[i:]
            return is_report_safe(damped_report)
    return True


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
