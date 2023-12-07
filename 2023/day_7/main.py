def load_plays(path):
    plays = []
    f = open(path)
    for line in f:
        split_line = line.split()
        plays.append({'hand': list(split_line[0]), 'bet': int(split_line[1])})
    f.close()
    return plays


def classify_hand(hand):
    card_counts = {}
    for card in hand:
        if card not in card_counts:
            card_counts[card] = 1
        else:
            card_counts[card] += 1

    print(card_counts)


def sum_winnings(path):
    sum = 0
    plays = load_plays(path)
    classify_hand(plays[0]['hand'])
    print(plays)
    return sum


def solve(path, part):
    if part == 1:
        sum = sum_winnings(path)
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
