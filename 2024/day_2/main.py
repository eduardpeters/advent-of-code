INCREASING = 1
DECREASING = -1


def solve(path: str, part: int) -> None:
    reports = get_reports(path)
    if part == 1:
        print("Getting levels")
        reports = parse_reports(reports)
        safe_count: int = 0
        for report in reports:
            if is_report_safe(report):
                safe_count += 1
        print(f"Safe Reports: {safe_count}")
    else:
        print("Solving Part two")


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
    report_trend = INCREASING if report[0] < report[1] else DECREASING
    for i in range(1, len(report)):
        if i != 1:
            trend = INCREASING if report[i - 1] < report[i] else DECREASING
            if trend != report_trend:
                return False
        diff = (
            report[i - 1] - report[i]
            if report_trend == DECREASING
            else report[i] - report[i - 1]
        )
        if diff < 1 or 3 < diff:
            return False
    return True


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
