import sys


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


ALPHABET = [' ', 'ა', 'ბ', 'გ', 'დ', 'ე', 'ვ', 'ზ', 'თ', 'ი', 'კ', 'ლ', 'მ', 'ნ', 'ო', 'პ', 'ჟ', 'რ', 'ს', 'ტ', 'უ',
            'ფ', 'ქ', 'ღ', 'ყ', 'შ', 'ჩ', 'ც', 'ძ', 'წ', 'ჭ', 'ხ', 'ჯ', 'ჰ']


def build_code_dict(code_file):
    code = {}

    for letter in ALPHABET:
        code_word = code_file.readline().rstrip('\n')
        code[letter] = code_word

    return code


def compress(codes, text_file, dest_file):
    buffer = ''

    while True:
        curr = text_file.read(1)

        if not curr:
            break

        buffer = buffer + codes[curr]

        if len(buffer) > 7:
            len_to_convert = len(buffer) - (len(buffer) % 8)
            to_bytes(buffer[:len_to_convert], dest_file)
            buffer = buffer[len_to_convert:]

    to_bytes(buffer, dest_file, True)


def process_files(file_names):
    code_file = open(file_names[0], 'r', encoding="utf8")
    text_file = open(file_names[1], 'r', encoding="utf8")
    dest_file = open(file_names[2], 'wb')

    codes = build_code_dict(code_file)
    compress(codes, text_file, dest_file)

    code_file.close()
    text_file.close()
    dest_file.close()


def main(argv):
    if len(argv) != 3:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
