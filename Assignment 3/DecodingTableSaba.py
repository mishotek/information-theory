import sys
from numpy import argsort, array, reshape, identity, concatenate
from itertools import combinations


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


def main(mx_fname, e_fname, dst_fname):
    # Read From File
    with open(mx_fname, 'r') as mf, open(e_fname, 'r') as ef:
        # Dimensions
        n, k = map(int, mf.readline().split())
        # Matrix
        mx = array(file_to_matrix(mf, k))
        # number e
        e = int(ef.read())
        # Permutations Array
        ps = array([i+1 for i in range(n)])
        # Standartization
        mx, ps = standartize(mx, ps, n, k)
        # Create P Matrix
        P = parity(mx, ps, n, k)

    dc = {}
    for tmp in range(e + 1):
        for subset in combinations(list(map(lambda x: x, range(n))), tmp):
            # print(subset)
            vec = [0] * n
            for i in subset:
                vec[i] = 1
            # print(vec)
            val = ''.join(map(str, P.dot(vec) % 2))
            if not val in dc:
                dc[val] = ''.join(map(str, vec))

    print(dc)

    # Write to File 
    with open(dst_fname, 'w+') as df:
        k = n- k
        df.write('{} {}\n'.format(n, k))
        for i in range(k):
            res = ''.join(map(str, P[i]))
            df.write('{}\n'.format(res))
        for val in dc:
            df.write("{}={}\n".format(val, dc[val]))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage : python3 Encode.py src-code src-fname dest-fname")
        exit()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
