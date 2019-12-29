import math
import sys


class Alphabet:

    arr = []

    def has(self, index):
        return len(self.arr) > index

    def push(self, elem):
        self.arr.append(elem)

    def get(self, index):
        return self.arr[index]

    def size(self):
        return len(self.arr)

    def replace(self, index, new_elem):
        self.arr[index] = new_elem

    def print(self):
        print(self.arr)


def to_bytes(string, dest_file, should_round=False):
    rounded = False
    index = 0

    while len(string) > index:
        index += 8
        byte = string[index - 8:index]

        if len(byte) != 8:
            byte = round_to_byte(byte)
            rounded = True
        dest_file.write(from_binary(byte))

    if not rounded and should_round:
        dest_file.write(from_binary('10000000'))


def round_to_byte(to_round):
    rounded = to_round + '1'

    if len(rounded) % 8 != 0:
        zeros_to_add = 8 - (len(rounded) % 8)

        for x in range(zeros_to_add):
            rounded += '0'

    return rounded


def from_binary(byte):
    return int(byte, 2).to_bytes(len(byte) // 8, byteorder='big')


def binary_to_decimal(binary):
    length = len(binary)
    decimal = 0

    for i in range(length):
        index = length - i - 1

        if binary[index] == '1':
            decimal = decimal + 2 ** i

    return decimal


def read_binary(source_file):
    buffer = ''

    while True:
        curr = source_file.read(1)

        if not curr:
            break

        buffer += to_binary(curr)

    last_index = buffer.rfind('1')

    return buffer[:last_index]


def to_binary(char):
    return ''.join('{0:08b}'.format(int(x), 'b') for x in char)


def extract_gamma(text):
    power = 0

    while text[power] == '0':
        power += 1

    return text[: power + power + 1]


def gamma_to_decimal(gamma_code):
    power = math.floor(len(gamma_code) / 2)
    left_over = binary_to_decimal(gamma_code[power + 1:])
    return math.floor(math.pow(2, power) + left_over)


def get_encoded_text(to_decompress):
    gamma_code = extract_gamma(to_decompress)
    start = len(gamma_code)

    return to_decompress[start:]


def is_code_word(word, alphabet):
    return math.ceil(math.log(alphabet.size(), 2)) == len(word)


def lz_decompress_word(word, alphabet):
    index = binary_to_decimal(word)
    decoded = alphabet.get(index)

    alphabet.replace(index, decoded + '0')
    alphabet.push(decoded + '1')
    return decoded


def lz_decompress(to_decompress):
    decompressed = ''

    alphabet = Alphabet()
    alphabet.push('0')
    alphabet.push('1')

    buffer = ''

    for char in to_decompress:
        buffer += char

        if is_code_word(buffer, alphabet):
            decompressed += lz_decompress_word(buffer, alphabet)
            buffer = ''

    return decompressed


def trim(string, gamma_code):
    text_length = gamma_to_decimal(gamma_code) * 8
    print(string[text_length - 100:])
    print(string)
    return string[:text_length]


def decompress(scr_file, dest_file):
    binary_file = read_binary(scr_file)
    to_decompress = get_encoded_text(binary_file)
    decompressed = trim(lz_decompress(to_decompress), extract_gamma(binary_file))
    to_bytes(decompressed, dest_file, True)


def process_files(file_names):
    scr_file = open(file_names[0], 'rb')
    dest_file = open(file_names[1], 'wb')

    decompress(scr_file, dest_file)

    scr_file.close()
    dest_file.close()


def main(argv):
    if len(argv) != 2:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


if __name__ == "__main__":
    main(sys.argv[1:])