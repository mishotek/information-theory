import sys
from StandardForm import standartize
from ParityCheck import parity
from Encode import file_to_str
from numpy import argsort, array, reshape
import itertools


def info_from_file(f, sz):
    matrix = f.read().split('\n')
    matrix, lines = matrix[:sz], matrix[sz:-1]
    matrix = list(map(list, matrix))
    for i in range(len(matrix)):
        s = matrix[i]
        matrix[i] = list(map(int, s))

    dc = {}
    for line in lines:
        parts = line.split('=')
        syn, code = parts[0], parts[1]
        dc[syn] = code
    return array(matrix), dc


def main(my_code_fname, input_fname, dst_fname):
    # Read From File
    with open(my_code_fname, 'r') as mf, open(input_fname, 'rb') as ef:
        # Dimensions
        n, k = map(int, mf.readline().split())
        # Matrix
        mx, dc = info_from_file(mf, k)
        # Read Recieved File to buffer
        file_data = file_to_str(ef)

    # Generate Data
    data_to_write = ''
    for i in range(len(file_data) // n):
        vec = array(list(map(int, file_data[i*n:(i + 1)*n]))).reshape((-1, 1))
        SENSHI = ''.join([str(c[0]) for c in mx.dot(vec) % 2])

        if SENSHI in dc:
            arr = array([int(c) for c in dc[SENSHI]]).reshape((-1, 1))
            vec = (vec - arr) % 2
            data_to_write += ''.join([str(v[0]) for v in vec])

    # Write to File
    with open(dst_fname, 'wb+') as df:
        ind, byte = 0, 0
        while True:
            for i in reversed(range(8)):
                if ind >= len(data_to_write):
                    df.write(bytes([byte | 2**i]))
                    return
                cur_bit = data_to_write[ind]
                ind += 1
                if cur_bit == '1':
                    byte |= 2 ** i
            df.write(bytes([byte]))
            byte = 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage : python3 Decode.py src-code src-fname dest-fname")
        exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
