import math
import sys


def str_to_nums(string):
    arr = []
    nums = string.split(' ')

    for arg in nums:
        if arg != '':
            arr.append(int(arg))

    return arr


def craft(numbers):
    res = 0

    for number in numbers:
        res = res + math.pow(0.5, number)

    return res


def build_code(numbers):
    res = []

    sorted_numbers = sorted(numbers)
    number = 0
    padding = 0

    for length in sorted_numbers:
        res.append(build_word(length, padding, number))

    return sorted_numbers


def process_files(file_names):
    source_file = open(file_names[0], 'r', encoding="utf8")
    dest_file = open(file_names[1], 'w', encoding="utf8")

    n = source_file.readline()
    numbers = str_to_nums(source_file.readline())
    craft_value = craft(numbers)

    if craft_value > 1:
        return

    code = build_code(numbers)
    print(numbers)
    print(code)

    source_file.close()
    dest_file.close()


def format_output(arg):
    return str(format(arg, '.7f'))


def main(argv):
    if len(argv) != 2:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
