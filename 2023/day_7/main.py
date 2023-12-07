FIVE_KIND = 7
FOUR_KIND = 6
FULL_HOUSE = 5
THREE_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0


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
    counts = list(card_counts.values())
    if 5 in counts:
        return FIVE_KIND
    if 4 in counts:
        return FOUR_KIND
    if 3 in counts:
        if 2 in counts:
            return FULL_HOUSE
        return THREE_KIND
    if counts.count(2) == 2:
        return TWO_PAIR
    if 2 in counts:
        return ONE_PAIR
    return HIGH_CARD


def sum_winnings(path):
    sum = 0
    plays = load_plays(path)
    print(plays)
    for play in plays:
        type = classify_hand(play['hand'])
        print(type)
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
