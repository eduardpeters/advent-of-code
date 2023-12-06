def get_int_list(string: str):
    return [int(x) for x in string.strip().split(':')[1].strip().split()]


def get_int_str(string: str):
    number_str = ''
    str_list = [x for x in string.strip().split(':')[1].strip().split()]
    return number_str.join(str_list)


def load_races(path):
    races = []
    f = open(path)
    times = get_int_list(f.readline())
    distances = get_int_list(f.readline())
    f.close()
    index = 0
    while index < len(times):
        races.append({'time': times[index], 'distance': distances[index]})
        index += 1
    return races


def load_single_race(path):
    races = []
    f = open(path)
    time = get_int_str(f.readline())
    distance = get_int_str(f.readline())
    f.close()
    return (time, distance)


def count_strategies(race):
    strategies = 0
    button_time = 1
    while button_time < race['time']:
        speed = button_time
        movement_time = race['time'] - button_time
        distance_traveled = speed * movement_time
        if distance_traveled > race['distance']:
            strategies += 1
        button_time += 1
    return strategies


def get_strategy_product(path):
    product = 1
    races = load_races(path)
    for race in races:
        product *= count_strategies(race)
    return product


def get_root_distance(path):
    distance = 1
    race = load_single_race(path)
    print(race)
    return distance


def solve(path, part):
    if part == 1:
        sum = get_strategy_product(path)
    else:
        sum = get_root_distance(path)
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
