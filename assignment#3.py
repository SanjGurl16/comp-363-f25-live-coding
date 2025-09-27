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

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def __str__(self):
        return f"({self.__symbol}:{self.__frequency})"

    def __repr__(self):
        return self.__str__()


# Filter message
def filter_uppercase_and_spaces(input_string: str) -> str:
    return "".join([char for char in input_string if char.isupper() or char == " "])


# Count frequencies
def count_frequencies(message: str) -> list[int]:
    ASCII_SYMBOLS = 256
    frequencies = [0] * ASCII_SYMBOLS
    for char in message:
        frequencies[ord(char)] += 1
    return frequencies


# Initialize forest
def initialize_forest(frequencies):
    forest = []
    for ascii_val in range(len(frequencies)):
        if frequencies[ascii_val] > 0:
            new_node = Node(frequencies[ascii_val], chr(ascii_val))
            forest.append(new_node)
    return forest


# Helper to get smallest node
def get_smallest(forest):
    smallest_index = 0
    for i in range(1, len(forest)):
        if forest[i] < forest[smallest_index]:
            smallest_index = i
    return forest.pop(smallest_index)


# Build Huffman tree
def build_huffman_tree(forest):
    while len(forest) > 1:
        s1 = get_smallest(forest)
        s2 = get_smallest(forest)
        new_node = Node(s1.get_frequency() + s2.get_frequency())
        new_node.set_left(s1)
        new_node.set_right(s2)
        forest.append(new_node)
    return forest[0]


# Generate Huffman codes
def generate_codes(node: Node, prefix: str = "", code_map=None) -> dict:
    if code_map is None:
        code_map = {}

    if node.get_symbol() is not None:  # Leaf node
        code_map[node.get_symbol()] = prefix
    else:
        if node.get_left():
            generate_codes(node.get_left(), prefix + "0", code_map)
        if node.get_right():
            generate_codes(node.get_right(), prefix + "1", code_map)
    return code_map


# Encode a message
def encode_message(message: str, codes: dict) -> str:
    return "".join(codes[char] for char in message)


# Decode a message
def decode_message(encoded: str, root: Node) -> str:
    decoded = []
    current = root
    for bit in encoded:
        if bit == "0":
            current = current.get_left()
        else:
            current = current.get_right()

        # If we hit a leaf node, append symbol
        if current.get_symbol() is not None:
            decoded.append(current.get_symbol())
            current = root
    return "".join(decoded)


# Example usage
if __name__ == "__main__":
    message_to_compress = "HELLO WORLD"
    filtered = filter_uppercase_and_spaces(message_to_compress)

    frequencies = count_frequencies(filtered)
    print("Frequencies:", frequencies)

    forest = initialize_forest(frequencies)
    print("Forest:", forest)

    huffman_tree = build_huffman_tree(forest)
    print("Root node:", huffman_tree)
    print("Root left:", huffman_tree.get_left())
    print("Root right:", huffman_tree.get_right())

    # Generate the Huffman table
    table = Node.generate_codes(huffman_tree)
    print("Huffman Table:", table)

    # Encode message
    encoded = encode_message(filtered, table)
    print("Encoded message:", encoded)

    # Decode message
    decoded = decode_message(encoded, table)
    print("Decoded message:", decoded)
