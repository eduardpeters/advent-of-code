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


def get_score(card):
    exponent = -1
    for number in card['winning']:
        if number in card['played']:
            exponent += 1
    score = 2**exponent if exponent >= 0 else 0
    return score


def sum_scores(path):
    sum = 0
    cards = load_cards(path)
    for card in cards:
        sum += get_score(card)
    return sum


def get_match_count(card):
    count = 0
    for number in card['winning']:
        if number in card['played']:
            count += 1
    return count


def sum_cards(path):
    cards = load_cards(path)
    card_count = [1] * len(cards)
    index = 0
    while index < len(cards):
        factor = card_count[index]
        score = get_match_count(cards[index])
        while score > 0:
            card_count[index + score] += factor
            score -= 1
        index += 1
    return sum(card_count)


def solve(path, part):
    if part == 1:
        sum = sum_scores(path)
    else:
        sum = sum_cards(path)
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
