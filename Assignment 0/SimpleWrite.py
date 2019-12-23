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

    while True:
        byte = source_file.read(8)
        if not byte:
            break
        dest_file.write(from_binary(byte))

    source_file.close()
    dest_file.close()


def from_binary(byte):
    return int(byte, 2).to_bytes(len(byte) // 8, byteorder='big')


if __name__ == "__main__":
    main(sys.argv[1:])