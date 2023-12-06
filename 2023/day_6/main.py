# Part 1 288 (4 * 8 * 9)
def get_int_list(string: str):
    return [int(x) for x in string.strip().split(':')[1].strip().split()]


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


def get_strategy_count(path):
    sum = 0
    races = load_races(path)
    print(races)
    return sum


def solve(path, part):
    if part == 1:
        sum = get_strategy_count(path)
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
