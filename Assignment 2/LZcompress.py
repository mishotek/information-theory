import math
import sys


class Alphabet:

    dict = {}
    index = 0

    def has(self, elem):
        return elem in self.dict

    def push(self, elem):
        i = self.index
        self.index = i + 1
        self.dict[elem] = i
        return i

    def get(self, elem):
        return self.dict[elem]


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


def to_bytes(string, dest_file, should_round = False):
    rounded = False

    while len(string) > 0:
        byte = string[:8]
        string = string[8:]
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


def elias_gama_code(number):
    result = ''

    power = math.floor(math.log(number, 2))
    left_over = decimal_to_binary(math.floor(number - math.pow(2, power)))

    while len(left_over) != power:
        left_over = '0' + left_over

    for i in range(0, power):
        result = result + '0'

    result = result + '1' + left_over
    return result


def decimal_to_binary(dec):
    return "{0:b}".format(dec)


def compress(scr_file, dest_file):
    to_compress = read_binary(scr_file)
    gama_code = elias_gama_code(len(to_compress))
    to_bytes(gama_code, dest_file)


def process_files(file_names):
    scr_file = open(file_names[0], 'rb')
    dest_file = open(file_names[1], 'wb')

    compress(scr_file, dest_file)

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