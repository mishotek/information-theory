import math
import sys


class QuerySet:

    def __init__(self, items):
        self.items = set(items)

    def of_length(self, length):
        for item in self.items:
            if len(item) is length:
                return item

    def pop(self, item):
        self.items.remove(item)


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


def decimal_to_binary(dec):
    return "{0:b}".format(dec)


def binary_to_decimal(binary):
    length = len(binary)
    decimal = 0

    for i in range(length):
        index = length - 1 - i

        if binary[index] == '1':
            decimal = decimal + 2 ** i

    return decimal


def increment_binary(binary):
    return decimal_to_binary(binary_to_decimal(binary) + 1)


def build_word(code_word, length):
    while len(code_word) < length:
        code_word = code_word + '0'
    return code_word


def increment_code(prev_code):
    if '1' not in prev_code:
        return prev_code[:len(prev_code) - 1] + '1'

    binary = increment_binary(prev_code[prev_code.index('1'):])

    while len(binary) < len(prev_code):
        binary = '0' + binary

    return binary


def build_code(numbers):
    res = []

    sorted_numbers = sorted(numbers)
    curr_code = '0'

    for length in sorted_numbers:
        code = build_word(curr_code, length)
        res.append(code)
        curr_code = increment_code(code)

    return res


def print_code(code, lengths, dest_file):
    items = QuerySet(code)

    for length in lengths:
        next_item = items.of_length(length)
        items.pop(next_item)
        dest_file.write(next_item + '\n')


def process_files(file_names):
    source_file = open(file_names[0], 'r', encoding="utf8")
    dest_file = open(file_names[1], 'w', encoding="utf8")

    n = source_file.readline()
    numbers = str_to_nums(source_file.readline())
    craft_value = craft(numbers)

    if craft_value > 1:
        return

    code = build_code(numbers)
    print_code(code, numbers, dest_file)

    source_file.close()
    dest_file.close()


def main(argv):
    if len(argv) != 2:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
