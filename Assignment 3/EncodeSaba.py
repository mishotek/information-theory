import sys
from numpy import argsort, array


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


def main(mx_fname, src_fname, dst_fname):

    with open(mx_fname) as mf:
        # Dimensions
        _, k = map(int, mf.readline().split())
        # Matrix
        mx = array(file_to_matrix(mf, k))

    with open(src_fname, 'rb') as sf, open(dst_fname, 'wb+') as df:
        file_data = file_to_str(sf)

        res = ''
        for i in range(len(file_data) // k):
            vec = array(list(map(int, file_data[i*k: (i+1)*k])))

            vec = vec.dot(mx) % 2
            print(vec)
            res += ''.join(list(map(str, vec)))

        ind, byte = 0,0 
        while True:
            for i in reversed(range(8)):
                if ind >= len(res):
                    df.write(bytes([byte | 2**i]))
                    return
                cur_bit = res[ind]
                ind += 1
                if cur_bit == '1':
                    byte |= 2 ** i
            df.write(bytes([byte]))
            byte = 0
                    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage : python3 Encode.py src-code src-fname dest-fname")
        exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
