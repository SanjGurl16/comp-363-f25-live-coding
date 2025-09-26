class Node:
    def __init__(self, frequency, symbol=None):
        self.__frequency = frequency
        self.__symbol = symbol
        self.__left = None
        self.__right = None

    def set_left(self, child):
        self.__left = child

    def set_right(self, child):
        self.__right = child

    def __lt__(self, other):
        return self.__frequency < other.__frequency

    def get_frequency(self) -> int:
        return self.__frequency

    def get_symbol(self) -> chr:
        return self.__symbol

    def __str__(self):
        return f"({self.__symbol}:{self.__frequency})"

    def __repr__(self):
        return self.__str__()

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    ASCII_SYMBOLS: int = 256


def frequency_of_symbols(message: str) -> list[int]:
    frequencies = [0] * ASCII_SYMBOLS
    for char in message:
        ascii_value = ord(char)
        frequencies[ascii_value] += 1
    return frequencies


def filter_uppercase_and_spaces(input_string):
    return "".join([char for char in input_string if char.isupper() or char == " "])


def create_forest(frequencies):
    forest = []
    for ascii in range(len(frequencies)):
        if frequencies[ascii] > 0:
            new_node = Node(frequencies[ascii], chr(ascii))
            forest.append(new_node)
    return forest


def get_smallest(forest):
    smallest_index = 0
    for i in range(1, len(forest)):
        if forest[i] < forest[smallest_index]:
            smallest_index = i
    return forest.pop(smallest_index)


def huffman(forest):
    while len(forest) > 1:
        s1 = get_smallest(forest)
        s2 = get_smallest(forest)
        new_node = Node(s1.get_frequency() + s2.get_frequency())
        new_node.set_left(s1)
        new_node.set_right(s2)
        forest.append(new_node)
    return forest[0]


message_to_compress = "HELLO WORLD"
filtered = filter_uppercase_and_spaces(message_to_compress)

frequencies = frequency_of_symbols(filtered)
print("Frequencies:", frequencies)

forest = create_forest(frequencies)
print("Forest:", forest)

huffman_tree = huffman(forest)
print("Root node:", huffman_tree)
print("Root left:", huffman_tree.get_left())
print("Root right:", huffman_tree.get_right())
