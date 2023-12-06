def parse_card(line):
    sides = line.split('|')
    winning = [int(x) for x in sides[0].split(':')[1].strip().split()]
    played = [int(x) for x in sides[1].strip().split()]
    return {'winning': winning, 'played': played}


def load_cards(path):
    cards = []
    f = open(path)
    for line in f:
        cards.append(parse_card(line))
    f.close()
    return cards


def sum_scores(path):
    sum = 0
    cards = load_cards(path)
    print(cards)
    return len(cards)


def solve(path, part):
    if part == 1:
        sum = sum_scores(path)
    else:
        sum = 1
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
