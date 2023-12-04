def load_matrix(path):
    matrix = []
    f = open(path)
    for line in f:
        print(line)
        matrix.append(line.split())
    f.close()
    return matrix


def sum_adjacent(path):
    sum = 0
    matrix = load_matrix(path)
    print(matrix)
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
