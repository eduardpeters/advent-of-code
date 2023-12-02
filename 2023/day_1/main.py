def get_code(path):
    sum = 0
    f = open(path)
    for line in f:
        num = None
        next = None
        for char in line:
            if char.isdigit():
                if num is None:
                    num = int(char)
                else:
                    next = int(char)
        if num:
            if next is None:
                next = num
            sum += num * 10 + next
    f.close()
    print(sum)


def is_potential_digit(char):
    return char == 'o' or char == 't' or char == 'f' or char == 's' or char == 'e' or char == 'n'


def parse_digit(str):
    if 'three' in str:
        return 3, 5
    if 'seven' in str:
        return 7, 5
    if 'eight' in str:
        return 8, 5
    if len(str) > 4:
        str = str[:-1]
    if 'four' in str:
        return 4, 4
    if 'five' in str:
        return 5, 4
    if 'nine' in str:
        return 9, 4
    if len(str) > 3:
        str = str[:-1]
    if 'one' in str:
        return 1, 3
    if 'two' in str:
        return 2, 3
    if 'six' in str:
        return 6, 3
    return None, 1


def get_code_letters(path):
    sum = 0
    f = open(path)
    for line in f:
        num = None
        next = None
        i = 0
        while i < len(line):
            if line[i].isdigit():
                if num is None:
                    num = int(line[i])
                else:
                    next = int(line[i])
                i += 1
            elif is_potential_digit(line[i]):
                value, length = parse_digit(line[i:i + 5])
                if value and num is None:
                    num = value
                elif value:
                    next = value
                i += length
            else:
                i += 1
        if num is not None:
            if next is None:
                next = num
            sum += num * 10 + next
    f.close()
    print(sum)


def choose_action():
    choice = int(
        input('0. Example One\n1. Part One\n2. Example Two\n3. Part Two\n-> '))
    if choice == 0:
        print('Running example part 1')
        get_code('example.txt')
    elif choice == 1:
        print('Running input part 1')
        get_code('input.txt')
    elif choice == 2:
        print('Running example part 2')
        get_code_letters('example_two.txt')
    else:
        print('Running input part 2')
        get_code_letters('input.txt')


if __name__ == "__main__":
    choose_action()
