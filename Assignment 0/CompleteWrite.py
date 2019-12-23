import sys


def main(argv):
    if len(argv) is not 2:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


def process_files(file_names):
    source_file = open(file_names[0], 'r')
    dest_file = open(file_names[1], 'wb')

    rounded = False

    while True:
        byte = source_file.read(8)
        if not byte:
            break
        if len(byte) is not 8:
            byte = round_to_byte(byte)
            rounded = True
        dest_file.write(from_binary(byte))

    if not rounded:
        dest_file.write(from_binary('10000000'))

    source_file.close()
    dest_file.close()


def to_bytes(string, dest_file):
    rounded = False

    while len(string) > 0:
        byte = string[:8]
        if len(byte) is not 8:
            byte = round_to_byte(byte)
            rounded = True
        dest_file.write(from_binary(byte))

    if not rounded:
        dest_file.write(from_binary('10000000'))


def round_to_byte(to_round):
    rounded = to_round + '1'

    if len(rounded) % 8 is not 0:
        zeros_to_add = 8 - (len(rounded) % 8)

        for x in range(zeros_to_add):
            rounded += '0'

    return rounded


def from_binary(byte):
    return int(byte, 2).to_bytes(len(byte) // 8, byteorder='big')


if __name__ == "__main__":
    main(sys.argv[1:])