import sys


class Node:

    value = None
    left = None
    right = None

    def is_leaf(self):
        return self.left is None and self.right is None


class PriorityQueue:

    items = []

    def push(self, item, priority):
        self.items.append((item, priority))

    def pop(self):
        lowest_priority = 1000000
        item = None
        index_to_remove = 0

        for index in range(0, len(self.items)):
            curr_item, curr_priority = self.items[index]

            is_new_lowest = lowest_priority > curr_priority

            item = curr_item if is_new_lowest else item
            lowest_priority = curr_priority if is_new_lowest else lowest_priority

            if is_new_lowest:
                index_to_remove = index

        if item is not Node:
            self.items.pop(index_to_remove)

        return item

    def length(self):
        return len(self.items)


def build_tree(nodes):
    queue = PriorityQueue()

    for node in nodes:
        queue.push(node, node.value)

    while queue.length() > 1:
        left_node = queue.pop()
        right_node = queue.pop()

        parent = Node()
        parent.left = left_node
        parent.right = right_node
        parent.value = left_node.value + right_node.value

        queue.push(parent, parent.value)

    return queue.pop()


def str_to_nums(string):
    nums = []
    strings = string.split(' ')

    for item in strings:
        nums.append(float(item))

    return nums


def to_nodes(numbers):
    nodes = []

    for num in numbers:
        node = Node()
        node.value = num
        nodes.append(node)

    return nodes


def build_code(frequencies):
    sorted_frequencies = sorted(frequencies)

    tree = build_tree(to_nodes(sorted_frequencies))
    print(tree.right.value)
    return tree


def process_files(file_names):
    source_file = open(file_names[0], 'r', encoding="utf8")
    dest_file = open(file_names[1], 'w', encoding="utf8")

    n = source_file.readline()
    numbers = str_to_nums(source_file.readline())

    code = build_code(numbers)

    source_file.close()
    dest_file.close()


def main(argv):
    if len(argv) != 2:
        print('Wrong arguments')
        return
    else:
        process_files(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
