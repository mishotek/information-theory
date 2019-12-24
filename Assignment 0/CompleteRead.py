import sys


def main(argv):
    if len(argv) is not 2:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


def process_files(file_names):
    source_file = open(file_names[0], 'rb')
    dest_file = open(file_names[1], 'w')

    buffer = ''

    while True:
        curr = source_file.read(1)

        if not curr:
            break

        buffer += to_binary(curr)

        buffer = write_from_buffer(buffer, dest_file)

    source_file.close()
    dest_file.close()


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


def write_from_buffer(buffer, dest):
    last_index = buffer.rfind('1')

    if last_index > 0:
        dest.write(buffer[:last_index])
        return buffer[last_index:]

    return buffer


if __name__ == "__main__":
    main(sys.argv[1:])
