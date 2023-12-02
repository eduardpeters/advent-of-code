def parse_game(runs):
    parsed_runs = []
    split_runs = runs.split(';')
    for run in split_runs:
        r = 0
        g = 0
        b = 0
        for cubes in run.strip().split(','):
            split_cubes = cubes.strip().split(' ')
            amount = int(split_cubes[0])
            color = split_cubes[1]
            if color == 'red':
                r += amount
            elif color == 'green':
                g += amount
            else:
                b += amount
        parsed_runs.append((r, g, b))
    return parsed_runs


def is_valid_game(game, max_red, max_green, max_blue):
    for run in game:
        if run[0] > max_red or run[1] > max_green or run[2] > max_blue:
            return False
    return True


def minimum_set(game):
    min_red = 0
    min_green = 0
    min_blue = 0
    for run in game:
        if run[0] > min_red:
            min_red = run[0]
        if run[1] > min_green:
            min_green = run[1]
        if run[2] > min_blue:
            min_blue = run[2]
    return (min_red, min_green, min_blue)


def get_power(rgb):
    power = 1
    for color in rgb:
        power *= color
    return power


def sum_valid(path):
    sum = 0
    game_id = 1
    f = open(path)
    for line in f:
        parsed_game = parse_game(line.split(':')[1].strip())
        print(parsed_game)
        if is_valid_game(parsed_game, 12, 13, 14):
            sum += game_id
        game_id += 1
    f.close()
    return sum


def sum_powers(path):
    sum = 0
    f = open(path)
    for line in f:
        parsed_game = parse_game(line.split(':')[1].strip())
        sum += get_power(minimum_set(parsed_game))
    f.close()
    return sum


def solve(path, part):
    if part == 1:
        sum = sum_valid(path)
    else:
        sum = sum_powers(path)
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
