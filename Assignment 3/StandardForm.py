import sys


class Matrix:

    rows = []

    def __init__(self, arrays):
        self.rows = arrays

    def print(self):
        for row in self.rows:
            for elem in row:
                print(elem, end=''),
            print()

    def print_diagonal(self):
        for i in range(0, self.get_row_count()):
            for j in range(0, self.get_row_count()):
                print(self.rows[i][j], end=''),
            print('')

    @staticmethod
    def subtract_rows(row1, row2):
        for i in range(0, len(row1)):
            row1[i] = abs(row1[i] - row2[i])

    def normalize(self):
        swap_table = self.init_swap_table(self.get_col_count())
        for row_index in range(0, len(self.rows)):
            self.normalize_row(row_index, self.rows, swap_table)

        return swap_table

    def normalize_row(self, row_index, rows, swap_table):
        self.set_one_on_diagonal(row_index, rows, swap_table)
        self.eliminate_in_others(row_index, rows)

    def set_one_on_diagonal(self, row_index, rows, swap_table):
        row = rows[row_index]
        has_one = row[row_index] == 1

        if has_one:
            return

        self.set_one(row_index, rows, swap_table)

    def set_one(self, row_index, rows, swap_table):
        cant_get_one_by_elimination = self.cant_get_one_by_elimination(rows, row_index)

        if cant_get_one_by_elimination:
            self.get_one_by_elimination(row_index, rows)
        else:
            self.swap_to_get_one(row_index, rows, swap_table)

    def swap_to_get_one(self, row_index, rows, swap_table):
        row = rows[row_index]
        index_to_swap = self.closest_index_of(row, 1, row_index + 1)
        self.swap_columns(rows, row_index, index_to_swap)
        self.swap_array(swap_table, row_index, index_to_swap)

    @staticmethod
    def cant_get_one_by_elimination(rows, index):
        for i in range(index + 1, len(rows)):
            row = rows[i]
            if row[index] == 1:
                return True
        return False

    def get_one_by_elimination(self, index, rows):
        row = rows[index]
        row_to_subtract = self.get_row_with_value(rows, index, 1)
        self.subtract_rows(row, row_to_subtract)

    @staticmethod
    def get_row_with_value(rows, index, value):
        for i in range(index + 1, len(rows)):
            row = rows[i]
            if row[index] == value:
                return row
        return None

    @staticmethod
    def closest_index_of(row, to_find, starting_index=0):
        for i in range(len(row), starting_index):
            if to_find == row[i]:
                return i
        return -1

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
    def swap_array(array, index1, index2):
        temp = array[index1]
        array[index1] = array[index2]
        array[index2] = temp

    def eliminate_in_others(self, row_index, rows):
        iterator = Matrix.Iterator(rows, [row_index])

        while True:
            row = iterator.next()

            if not row:
                return

            if row[row_index] == 1:
                self.subtract_rows(row, rows[row_index])

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

        self.print_diagonal()


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
