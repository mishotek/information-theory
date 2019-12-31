import sys
from numpy import array, concatenate


# ამ დავალების დაწერაში საბა ფოჩხუამ დამეხმარა და numpy იც მაგან დამაყენებინა
# და შესაბამისათ ერეიზე ის პითონიზმებიც მან მასწავლა და შეიძლება დაემთხვეს


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
        swap_table = self.init_swap_table(self.get_col_count())

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
            swap_table.append(i + 1)

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

    def write(self, dest_file, swap_table):
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

        for index in swap_table:
            dest_file.write(str(index))
            dest_file.write(' ')

    def to_parity_matrix(self):
        rvrs = self.rows[:, self.get_row_count():].T
        identity_matrix = Matrix.build_identity(self.get_col_count() - self.get_row_count())
        self.rows = concatenate((rvrs, identity_matrix), axis=1)

    @staticmethod
    def build_identity(size):
        arr = []

        for i in range(0, size):
            inner = []
            for j in range(0, size):
                inner.append(0)
            arr.append(inner)

        for i in range(0, size):
            arr[i][i] = 1

        return arr


def read_meta_data(line):
    return int(line.split(' ')[0]), int(line.split(' ')[1])


def build_matrix(scr_file):
    rows = []

    while True:
        row_str = scr_file.readline().rstrip('\n')

        if not row_str:
            return Matrix(rows)

        row = []

        for char in row_str:
            row.append(int(char))

        rows.append(row)


def process_files(file_names):
    scr_file = open(file_names[0], 'r')
    dest_file = open(file_names[1], 'w')

    col_count, row_count = read_meta_data(scr_file.readline())
    matrix = build_matrix(scr_file)
    swap_table = matrix.normalize()
    matrix.to_parity_matrix()

    matrix.write(dest_file, swap_table)

    scr_file.close()
    dest_file.close()


def main(argv):
    if len(argv) != 2:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
