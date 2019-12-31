import sys
from numpy import array, argsort, concatenate, identity
from StandardForm import file_to_matrix, standartize


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
