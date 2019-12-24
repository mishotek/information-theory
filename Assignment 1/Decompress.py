import sys


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


ALPHABET = [' ', 'ა', 'ბ', 'გ', 'დ', 'ე', 'ვ', 'ზ', 'თ', 'ი', 'კ', 'ლ', 'მ', 'ნ', 'ო', 'პ', 'ჟ', 'რ', 'ს', 'ტ', 'უ',
            'ფ', 'ქ', 'ღ', 'ყ', 'შ', 'ჩ', 'ც', 'ძ', 'წ', 'ჭ', 'ხ', 'ჯ', 'ჰ']


def build_code_dict(code_file):
    code = {}

    for letter in ALPHABET:
        code_word = code_file.readline().rstrip('\n')
        code[code_word] = letter

    return code


def decompress(codes, text_file, dest_file):
    binary = read_binary(text_file)

    while len(binary) > 0:
        code = ''

        while code not in codes:
            code = code + binary[0]
            binary = binary[1:]

        dest_file.write(codes[code])


def process_files(file_names):
    code_file = open(file_names[0], 'r', encoding="utf8")
    text_file = open(file_names[1], 'rb')
    dest_file = open(file_names[2], 'w', encoding="utf8")

    codes = build_code_dict(code_file)
    decompress(codes, text_file, dest_file)

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