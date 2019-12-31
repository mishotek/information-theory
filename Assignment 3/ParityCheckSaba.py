import sys
from numpy import array, argsort, concatenate, identity


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


def parity(mx, ps, n, k):
    mx = mx[:, k:].T
    I = identity(n - k, int)
    tmp = concatenate((mx, I), axis=1)
    res = tmp[:, argsort(ps)]
    return res


def main(src_fname, dst_fname):
    with open(src_fname, 'r') as sf, open(dst_fname, 'w+') as df:
        # Dimensions
        n, k = map(int, sf.readline().split())
        # Matrix
        mx = array(file_to_matrix(sf, k))
        # Permutations Array
        ps = array([i+1 for i in range(n)])
        # Standartization
        mx, ps = standartize(mx, ps, n, k)
        # Create P Matrix
        P = parity(mx, ps, n, k)
        # Write to File
        df.write('{} {}\n'.format(n, n - k))
        for row in P:
            vector = ''.join(map(str, row))
            df.write('{}\n'.format(vector))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python3 Decode.py  src-code src-fname dest-fname")
        exit()
    main(sys.argv[1], sys.argv[2])
