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

    while True:
        char = source_file.read(1)
        if not char:
            break
        dest_file.write(to_binary(char))

    source_file.close()
    dest_file.close()


def to_binary(char):
    return ''.join('{0:08b}'.format(int(x), 'b') for x in char)


if __name__ == "__main__":
    main(sys.argv[1:])
