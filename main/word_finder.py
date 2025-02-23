import os

# Define the letter point mapping.
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


grid = [
    ['L', 'V', 'O', 'L', 'E'],
    ['O', 'A', 'D', 'K', 'E'],
    ['V', 'O', 'B', 'S', 'O'],
    ['R', 'F', 'T', 'N', 'E'],
    ['I', 'A', 'N', 'D', 'I']
]
ROWS, COLS = 5, 5
