import sys

from numpy import argsort, array, reshape, identity, concatenate
import itertools

def parity(mx, ps, n, k):
    mx = mx[:, k:].T
    I = identity(n - k, int)
    tmp = concatenate((mx, I), axis=1)
    res = tmp[:, argsort(ps)]
    return res


def file_to_matrix(f, sz):
    matrix = []
    matrix = f.read().split('\n')[:sz]
    matrix = list(map(list, matrix))
    for i in range(len(matrix)):
        s = matrix[i]
        matrix[i] = list(map(int, s))
    return matrix


def standartize(mx, ps, n, k):
    for i in range(k):
        if mx[i, i] == 0:
            done = False
            for j in range(i + 1, k):
                if mx[j, i] == 1:
                    mx[[i, j]], done = mx[[j, i]], True
                    break
            if not done:
                for j in range(i + 1, n):
                    if mx[i, j] == 1:
                        mx[:, [i, j]], ps[[i, j]] = mx[:, [j, i]], ps[[j, i]]
                        break
        for j in range(k):
            if j != i and mx[j, i] == 1:
                mx[j, :] ^= mx[i, :]
    return mx, ps


def file_to_str(sf):
    res = ''
    while True:
        buf = sf.read(1024)
        if buf:
            for byte in buf:
                byte_str = "{0:{f}8b}".format(byte, f='0')
                res += byte_str
        else:
            break
    return res



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

    print(data_to_write)
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
