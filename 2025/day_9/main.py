from dataclasses import dataclass

EMPTY = "."
VALID = "#"


@dataclass
class CompactTiles:
    grid: list[list[str]]
    map_x: dict[int, int]
    map_y: dict[int, int]
    max_x: int
    max_y: int
    max_x_original: int
    max_y_original: int
    min_x = 0
    min_y = 0

    def is_contained(self, vertex: tuple[int, int]) -> bool:
        scaled_vertex = self._scaled_vertex(vertex)
        x, y = scaled_vertex
        return self.grid[y][x] == VALID

    def _scaled_vertex(self, vertex: tuple[int, int]) -> tuple[int, int]:
        return (self.map_x[vertex[0]], self.map_y[vertex[1]])

    def is_perimeter_valid(
        self,
        a: tuple[int, int],
        b: tuple[int, int],
        c: tuple[int, int],
        d: tuple[int, int],
    ) -> bool:
        scaled_a = self._scaled_vertex(a)
        scaled_b = self._scaled_vertex(b)
        scaled_c = self._scaled_vertex(c)
        scaled_d = self._scaled_vertex(d)

        min_x, min_y = scaled_a
        max_x, max_y = scaled_a
        for v in [scaled_b, scaled_c, scaled_d]:
            if v[0] < min_x:
                min_x = v[0]
            elif v[0] > max_x:
                max_x = v[0]
            if v[1] < min_y:
                min_y = v[1]
            elif v[1] > max_y:
                max_y = v[1]

        for row in range(min_y, max_y + 1):
            for column in range(min_x, max_x + 1):
                if self.grid[row][column] != VALID:
                    return False

        return True


def side_length(a: int, b: int) -> int:
    return abs(a - b) + 1


def rectangle_area(a: tuple[int, int], b: tuple[int, int]) -> int:
    return side_length(a[0], b[0]) * side_length(a[1], b[1])


def get_missing_rectangle_vertices(
    a: tuple[int, int], c: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    return (c[0], a[1]), (a[0], c[1])


def has_valid(
    grid: list[list[str]], row: int, column: int, delta_row: int, delta_column: int
) -> bool:
    if row < 0 or row >= len(grid) or column < 0 or column >= len(grid[row]):
        return False

    if grid[row][column] == VALID:
        return True

    return has_valid(
        grid, row + delta_row, column + delta_column, delta_row, delta_column
    )


def is_enclosed(grid: list[list[str]], row: int, column: int) -> bool:
    if grid[row][column] == VALID:
        return True
    # Check if enclosed on all sides
    return (
        has_valid(grid, row, column, -1, 0)
        and has_valid(grid, row, column, 1, 0)
        and has_valid(grid, row, column, 0, -1)
        and has_valid(grid, row, column, 0, 1)
    )


def compact_tiles(
    tiles: list[tuple[int, int]],
) -> CompactTiles:
    sorted_x = sorted({x for x in [t[0] for t in tiles]})
    sorted_y = sorted({y for y in [t[1] for t in tiles]})
    compacted_tiles: list[tuple[int, int]] = []
    for tile in tiles:
        compacted = (sorted_x.index(tile[0]), sorted_y.index(tile[1]))
        compacted_tiles.append(compacted)

    grid: list[list[str]] = [[EMPTY for _ in sorted_x] for _ in sorted_y]
    for i, a in enumerate(compacted_tiles):
        if i == len(compacted_tiles) - 1:
            b = compacted_tiles[0]
        else:
            b = compacted_tiles[i + 1]
        if a[0] == b[0]:
            if a[1] < b[1]:
                start = a[1]
                end = b[1]
            else:
                start = b[1]
                end = a[1]
            col = a[0]
            for row in range(start, end + 1):
                grid[row][col] = VALID
        else:
            row = a[1]
            if a[0] < b[0]:
                start = a[0]
                end = b[0]
            else:
                start = b[0]
                end = a[0]
            for col in range(start, end + 1):
                grid[row][col] = VALID
    # Fill in inner area as valid
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if is_enclosed(grid, row, column):
                grid[row][column] = VALID

    return CompactTiles(
        grid=grid,
        map_x={x: i for i, x in enumerate(sorted_x)},
        map_y={y: i for i, y in enumerate(sorted_y)},
        max_x=len(sorted_x) - 1,
        max_y=len(sorted_y) - 1,
        max_x_original=sorted_x[-1],
        max_y_original=sorted_y[-1],
    )


def solve(path: str, part: int) -> None:
    tiles = load_file(path)

    max_area = 1
    if part == 1:
        print("Solving for part 1")
        for i, pivot in enumerate(tiles):
            for opposite in tiles[i + 1 :]:
                area = rectangle_area(pivot, opposite)
                if area > max_area:
                    max_area = area
    else:
        print("Solving for part 2")
        compacted = compact_tiles(tiles)
        for i, tile_a in enumerate(tiles):
            for tile_c in tiles[i + 1 :]:
                area = rectangle_area(tile_a, tile_c)
                if area > max_area:
                    tile_b, tile_d = get_missing_rectangle_vertices(tile_a, tile_c)
                    if (
                        compacted.is_contained(tile_b)
                        and compacted.is_contained(tile_d)
                        and compacted.is_perimeter_valid(tile_a, tile_b, tile_c, tile_d)
                    ):
                        max_area = area

    print(f"Max area found: {max_area}")


def load_file(path: str) -> list[tuple[int, int]]:
    tiles: list[tuple[int, int]] = []

    with open(path) as file:
        for line in file:
            x, y = line.strip().split(",")
            tiles.append((int(x), int(y)))

    return tiles


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
