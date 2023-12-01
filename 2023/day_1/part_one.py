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
      if num is not None:
        if next is None:
           next = num
        sum += num * 10 + next
    f.close()
    print(sum)

def choose_action():
    choice = int(input('0. Example\n1. Input\n-> '))
    if choice == 0:
        print('Running example')
        get_code('example.txt')
    else:
        print('Running input')
        get_code('input.txt')

if __name__ == "__main__":
    choose_action()