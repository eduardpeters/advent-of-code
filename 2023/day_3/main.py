def load_matrix(path):
    matrix = []
    f = open(path)
    for line in f:
        print(line)
        matrix.append(list(line[:-1]))
    f.close()
    return matrix


def get_part_number(matrix, row, column):
    offset = 1
    number_str = matrix[row][column]
    while matrix[row][column + offset].isdigit():
        number_str += matrix[row][column + offset]
        offset += 1
    print(number_str)
    return (int(number_str), offset)


def sum_adjacent(path):
    sum = 0
    matrix = load_matrix(path)
    print(matrix)
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
