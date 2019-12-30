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

    @staticmethod
    def subtract_rows(row1, row2):
        for i in range(0, len(row1)):
            row1[i] = abs(row1[i] - row2[i])

    def normalize(self):
        swap_table = self.init_swap_table(self.get_col_count())
        for row_index in range(0, len(self.rows)):
            self.normalize_row(row_index, self.rows, swap_table)

        print(swap_table)

    def normalize_row(self, row_index, rows, swap_table):
        row = rows[row_index]

        has_one = row[row_index] == 1

        if not has_one:
            self.swap_to_get_one(row_index, rows, swap_table)

        self.elimination(self, row_index, rows)

    def swap_to_get_one(self, row_index, rows, swap_table):
        row = rows[row_index]
        index_to_swap = self.closest_index_of(row, 1, row_index + 1)
        self.swap_columns(rows, row_index, index_to_swap)
        self.swap_array(swap_table, row_index, index_to_swap)

    @staticmethod
    def closest_index_of(row, to_find, starting_index=0):
        for i in range(starting_index, len(row)):
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

    def elimination(self, self1, row_index, rows):
        return 0


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
    matrix.normalize()
    matrix.print()

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
