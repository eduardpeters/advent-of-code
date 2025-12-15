from dataclasses import dataclass, field

SHAPE = "#"
FREE = "."
PRESENT_MAX_AREA = 9


@dataclass
class Present:
    index: int
    shape: list[str]
    area: int = field(init=False)

    def __post_init__(self):
        area = 0
        for row in self.shape:
            for column in row:
                if column == SHAPE:
                    area += 1
        self.area = area


@dataclass
class Region:
    width: int
    height: int
    area: int = field(init=False)
    presents: list[int]

    def __post_init__(self):
        self.area = self.width * self.height


def solve(path: str, part: int) -> None:
    presents, regions = load_file(path)

    if part == 1:
        print("Solving for part 1")
        total_regions = len(regions)
        larger_regions = 0
        smaller_regions = 0
        arrange_regions = 0
        for region in regions:
            max_present_area = PRESENT_MAX_AREA * sum(region.presents)
            min_present_area = 0
            for idx_present, number_presents in enumerate(region.presents):
                min_present_area += number_presents * presents[idx_present].area
            if region.area < min_present_area:
                smaller_regions += 1
            elif max_present_area <= region.area:
                larger_regions += 1
            else:
                arrange_regions += 1
        print(f"Total regions: {total_regions}")
        print(f"Too small for presents: {smaller_regions}")
        print(f"Need arrangement: {arrange_regions}")
        print(f"No arrangement needed: {larger_regions}")
    else:
        print("Solving for part 2")


def load_file(path: str) -> tuple[list[Present], list[Region]]:
    presents: list[Present] = []
    regions: list[Region] = []

    with open(path) as file:
        current_present: Present | None = None

        for line in file:
            clean_line = line.strip()
            if current_present:
                if clean_line:
                    current_present.shape.append(clean_line)
                else:
                    present = Present(
                        index=current_present.index, shape=current_present.shape
                    )
                    presents.append(present)
                    current_present = None
            else:
                if "x" in clean_line:
                    dimensions, present_indices = clean_line.split(": ")
                    width, height = dimensions.split("x")
                    region = Region(
                        width=int(width),
                        height=int(height),
                        presents=[int(p) for p in present_indices.split()],
                    )
                    regions.append(region)
                else:
                    current_present = Present(index=int(clean_line[:-1]), shape=[])

    return (presents, regions)


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
        solve("example_2.txt", 2)
    else:
        print("Running input part 2")
        solve("input.txt", 2)


if __name__ == "__main__":
    choose_action()
