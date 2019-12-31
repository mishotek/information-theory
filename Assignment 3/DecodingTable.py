import sys
from itertools import combinations

from numpy import array, concatenate, argsort


class Matrix:

    rows = []

    def __init__(self, arrays):
        self.rows = array(arrays)

    def print(self):
        for row in self.rows:
            for elem in row:
                print(elem, end=''),
            print()

    def normalize(self):
        swap_table = array(self.init_swap_table(self.get_col_count()))

        for row_index in range(0, self.get_row_count()):
            has_one = self.rows[row_index, row_index] == 1

            if not has_one:
                can_get_one_by_elimination = self.can_get_one_by_elimination(row_index)
                if can_get_one_by_elimination:
                    self.set_one_by_elimination(row_index)
                else:
                    self.set_one_by_swapping(row_index, swap_table)

            self.eliminate(row_index)

        return swap_table

    def get_elimination_row(self, elem_index):
        starting_index = elem_index + 1

        for row_index in range(starting_index, self.get_row_count()):
            has_one_to_eliminate = self.rows[row_index, elem_index] == 1

            if has_one_to_eliminate:
                return row_index

        return -1

    def can_get_one_by_elimination(self, elem_index):
        return self.get_elimination_row(elem_index) != -1

    def set_one_by_elimination(self, elem_index):
        row_to_eliminate = self.get_elimination_row(elem_index)
        self.rows[[elem_index, row_to_eliminate]] = self.rows[[row_to_eliminate, elem_index]]

    def set_one_by_swapping(self, row_index, swap_table):
        col_index = self.get_swap_col_index(row_index)
        self.swap_columns(self.rows, row_index, col_index)
        self.swap_array(swap_table, row_index, col_index)

    def get_swap_col_index(self, row_index):
        for col_index in range(row_index + 1, self.get_col_count()):
            if self.rows[row_index, col_index] == 1:
                return col_index
        return -1

    def eliminate(self, row_index):
        for j in range(0, self.get_row_count()):
            if j != row_index and self.rows[j, row_index] == 1:
                self.rows[j, :] ^= self.rows[row_index, :]

    def get_col_count(self):
        if len(self.rows) == 0:
            return 0
        return len(self.rows[0])

    @staticmethod
    def init_swap_table(length):
        swap_table = []

        for i in range(0, length):
            swap_table.append(i)

        return swap_table

    def swap_columns(self, rows, index1, index2):
        for row in rows:
            self.swap_array(row, index1, index2)

    @staticmethod
    def swap_array(arr, index1, index2):
        temp = arr[index1]
        arr[index1] = arr[index2]
        arr[index2] = temp

    def get_row_count(self):
        return len(self.rows)

    class Iterator:

        def __init__(self, rows, rows_to_skip=[]):
            self.rows = rows
            self.rows_to_skip = rows_to_skip
            self.index = self.get_initial_index(len(rows), rows_to_skip)

        def next(self):
            if self.index != -1 and len(self.rows) > self.index:
                index = self.index
                self.index = self.get_next_index(len(self.rows), self.rows_to_skip)
                return self.rows[index]
            return None

        @staticmethod
        def get_initial_index(length, rows_to_skip):
            for i in range(0, length + 1):
                if i not in rows_to_skip:
                    return i
            return -1

        def get_next_index(self, length, rows_to_skip):
            for i in range(self.index + 1, length + 1):
                if i not in rows_to_skip:
                    return i
            return -1

    def write(self, dest_file):
        dest_file.write(str(self.get_col_count()))
        dest_file.write(' ')
        dest_file.write(str(self.get_row_count()))
        dest_file.write('\n')

        iterator = Matrix.Iterator(self.rows)

        while True:
            row = iterator.next()

            if row is None:
                break

            for num in row:
                dest_file.write(str(num))
            dest_file.write('\n')

    def to_parity_matrix(self, swap_table):
        # აქ რაც numpy-ის რაღაცეები მაქვს გამოყენებული საბამ ჩამიგდო
        # და შესაძლოა მის დავალებას დაემთხვეს რაღაც ნაწილი, რაგან როგორც
        # მითხრა "ამეებს ვიყენებო და ბევრი არ იწვალო შენით დასაწერი არააო
        # პითონს აქვს ტავისიო და მოყვებაო"
        rotated_matrix = self.rows[:, self.get_row_count():].T
        i_matrix = self.get_i_matrix(self.get_col_count() - self.get_row_count())
        tmp = concatenate((rotated_matrix, i_matrix), axis=1)
        res = tmp[:, argsort(swap_table)]
        self.rows = array(res)

    def get_to_rotate(self, size):
        res = []

        starting_index = self.get_col_count() - size

        iterator = Matrix.Iterator(self.rows)

        while True:
            row = iterator.next()

            if row is None:
                return res

            res.append(row[starting_index:])

    @staticmethod
    def matrix_of_size(rows, cols, val=0):
        res = []

        for r in range(0, rows):
            arr = []
            for c in range(0, cols):
                arr.append(val)
            res.append(arr)

        return res

    def rotated_matrix(self, to_rotate):
        cols = len(to_rotate)
        rows = len(to_rotate[0])

        res = self.matrix_of_size(rows, cols)

        for r in range(0, cols):
            for c in range(0, rows):
                res[c][r] = to_rotate[r][c]

        return res

    def get_i_matrix(self, size):
        res = self.matrix_of_size(size, size)
        for i in range(0, size):
            res[i][i] = 1

        return res

    def join(self, m1, m2):
        res = self.matrix_of_size(len(m1), len(m1[0]) + len(m2[0]))

        for r in range(0, len(m1)):
            for c in range(0, len(m1[0])):
                res[r][c] = m1[r][c]

        for r in range(0, len(m2)):
            for c in range(0, len(m2[0])):
                res[r][c + len(m1[0])] = m1[r][c]

        return res


def read_meta_data(line):
    return int(line.split(' ')[0]), int(line.split(' ')[1])


def read_rows(scr_file):
    rows = []

    while True:
        row_str = scr_file.readline().rstrip('\n')

        if not row_str:
            return rows

        row = []

        for char in row_str:
            row.append(int(char))

        rows.append(row)


def subset_to_vector(subset, matrix):
    vector = matrix.matrix_of_size(1, matrix.get_col_count(), 0)[0]

    for index in subset:
        vector[index] = 1

    return vector


def to_string(vector):
    string = ''

    for num in vector:
        string += str(num)

    return string


def store_code(code, vector, tree):
    vector_as_str = to_string(vector)
    tree[code] = vector_as_str


def build_coding_tree_over_subsets(matrix, distance, tree):

    def identity(index):
        return index

    for subset in combinations(list(map(identity, range(0, matrix.get_col_count()))), distance):
        vector = subset_to_vector(subset, matrix)
        code = ''.join(map(str, matrix.rows.dot(vector) % 2))

        if code not in tree:
            store_code(code, vector, tree)


def build_coding_tree(matrix, distances):
    tree = {}

    for distance in range(0, distances):
        build_coding_tree_over_subsets(matrix, distance, tree)

    return tree


def read_e(e_file):
    return int(e_file.readline())


def write_dictionary(dst_file, dictionary):
    dst_file.write('{\n')

    for key in dictionary:
        dst_file.write(key)
        dst_file.write(': ')
        dst_file.write(dictionary[key])
        dst_file.write(',\n')

    dst_file.write('}\n')


def process_files(file_names):
    scr_file = open(file_names[0], 'r')
    e_file = open(file_names[1], 'r')
    dest_file = open(file_names[2], 'w')

    read_meta_data(scr_file.readline())
    rows = read_rows(scr_file)
    matrix = Matrix(rows)
    e = read_e(e_file)
    swap_table = matrix.normalize()
    matrix.to_parity_matrix(swap_table)

    codes = build_coding_tree(matrix, e + 1)
    original_matrix = Matrix(rows)

    original_matrix.write(dest_file)

    write_dictionary(dest_file, codes)

    scr_file.close()
    e_file.close()
    dest_file.close()


def main(argv):
    if len(argv) != 3:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
