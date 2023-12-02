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


def sum_valid(path):
    sum = 0
    game_id = 1
    f = open(path)
    for line in f:
        parsed_game = parse_game(line.split(':')[1].strip())
        if is_valid_game(parsed_game, 12, 13, 14):
            sum += game_id
        game_id += 1
    f.close()
    return sum


def solve_part_one(path):
    sum = sum_valid(path)
    print(sum)


def choose_action():
    choice = int(
        input('0. Example One\n1. Part One\n2. Example Two\n3. Part Two\n-> '))
    if choice == 0:
        print('Running example part 1')
        solve_part_one('example.txt')
    elif choice == 1:
        print('Running input part 1')
        solve_part_one('input.txt')
    elif choice == 2:
        print('Running example part 2')
    else:
        print('Running input part 2')


if __name__ == "__main__":
    choose_action()
