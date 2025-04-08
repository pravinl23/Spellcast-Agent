# Define the letter point mapping
score_mapping = {
    'A': 1, 'E': 1, 'I': 1, 'O': 1,
    'N': 2, 'R': 2, 'S': 2, 'T': 2,
    'D': 3, 'G': 3, 'L': 3,
    'B': 4, 'H': 4, 'P': 4, 'M': 4, 'U': 4, 'Y': 4,
    'C': 5, 'F': 5, 'V': 5, 'W': 5,
    'K': 6,
    'J': 7, 'X': 7,
    'Q': 8, 'Z': 8
}

# Directions the path can move 
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def load_dictionary(dictionary_path):
    with open(dictionary_path, 'r') as f:
        # For each line in the dictionary, strip whitespace, convert to uppercase
        words = [w.strip().upper() for w in f]

    # Create an empty set for all valid prefixes
    prefix_set = set()

    for word in words:
        # Generate all prefixes for each word
        for i in range(1, len(word)+1):
            prefix_set.add(word[:i])

    # Return both the list of words and all possible prefixes
    return words, prefix_set
