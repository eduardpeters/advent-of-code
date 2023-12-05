def load_matrix(path):
    matrix = []
    f = open(path)
    for line in f:
        matrix.append(list(line[:-1]))
    f.close()
    return matrix


def symbol_above(matrix, upper_row, left_column, right_column):
    if upper_row < 0:
        return False
    c = left_column if left_column >= 0 else 0
    limit = right_column if right_column < len(
        matrix[upper_row]) else right_column - 1
    while c <= limit:
        if matrix[upper_row][c] != '.':
            return True
        c += 1
    return False


def symbol_on_side(matrix, row, left_column, right_column):
    if left_column >= 0:
        if matrix[row][left_column] != '.':
            return True
    if right_column < len(matrix[row]):
        if matrix[row][right_column] != '.':
            return True
    return False


def symbol_below(matrix, lower_row, left_column, right_column):
    if lower_row >= len(matrix):
        return False
    c = left_column if left_column >= 0 else 0
    limit = right_column if right_column < len(
        matrix[lower_row]) else right_column - 1
    while c <= limit:
        if matrix[lower_row][c] != '.':
            return True
        c += 1
    return False


def is_adjacent(matrix, row, column, offset):
    upper_row = row - 1
    left_column = column - 1
    lower_row = row + 1
    right_column = column + offset + 1
    if symbol_above(matrix, upper_row, left_column, right_column):
        return True
    if symbol_on_side(matrix, row, left_column, right_column):
        return True
    if symbol_below(matrix, lower_row, left_column, right_column):
        return True
    return False


def get_part_number(matrix, row, column):
    part_number = 0
    offset = 1
    number_str = matrix[row][column]
    while column + offset < len(matrix[row]) and matrix[row][column + offset].isdigit():
        number_str += matrix[row][column + offset]
        offset += 1
    offset -= 1
    if (is_adjacent(matrix, row, column, offset)):
        part_number = int(number_str)
    return (part_number, offset)


def sum_adjacent(path):
    sum = 0
    matrix = load_matrix(path)
    row = 0
    while row < len(matrix):
        column = 0
        while column < len(matrix[row]):
            if matrix[row][column].isdigit():
                number, offset = get_part_number(matrix, row, column)
                sum += number
                column += offset
            column += 1
        row += 1
    return sum


def solve(path, part):
    if part == 1:
        sum = sum_adjacent(path)
    else:
        sum = 0
    print(sum)


def choose_action():
    choice = int(
        input('0. Example One\n1. Part One\n2. Example Two\n3. Part Two\n-> '))
    if choice == 0:
        print('Running example part 1')
        solve('example.txt', 1)
    elif choice == 1:
        print('Running input part 1')
        solve('input.txt', 1)
    elif choice == 2:
        print('Running example part 2')
        solve('example.txt', 2)
    else:
        print('Running input part 2')
        solve('input.txt', 2)


if __name__ == "__main__":
    choose_action()
