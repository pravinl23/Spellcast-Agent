from export_grid import export_grid

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

def calculate_word_score(word):
    # Base score from letter values
    base_score = 0
    for letter in word:
        if letter in score_mapping:
            base_score += score_mapping[letter]
    
    # Apply length bonuses
    length = len(word)
    if length <= 2:
        return base_score
    elif length == 3 or length == 4:
        return base_score + 1
    elif length == 5:
        return base_score + 2
    elif length == 6:
        return base_score + 3
    elif length == 7:
        return base_score + 5
    else:
        return base_score + 11

def is_valid_position(grid, row, col):
    if row >= 0 and row < len(grid):
        if col >= 0 and col < len(grid[0]):
            return True
        else:
            return False
    else:
        return False

def find_words(grid, dictionary_words, prefix_set):
    rows, cols = len(grid), len(grid[0])
    found_words = []
    
    # Convert dictionary_words to a set for faster lookups
    dictionary_set = set(dictionary_words)
    
    def dfs(row, col, current_word, path, visited):
        # Check if current position is valid
        if not is_valid_position(grid, row, col) or (row, col) in visited:
            return
        
        # Add current letter to the word
        current_word += grid[row][col]
        
        # Check if the current word is a valid prefix if not return
        if current_word not in prefix_set:
            return
        
        # Track visited positions to avoid using same cell twice
        visited.add((row, col))
        path.append((row, col))
        
        # If we have a valid word (at least 3 letters), add it to found words
        if current_word in dictionary_set and len(current_word) >= 3:
            score = calculate_word_score(current_word)
            found_words.append((current_word, score, path.copy()))
        
        # Explore all possible directions
        for dr, dc in DIRECTIONS:
            dfs(row + dr, col + dc, current_word, path, visited.copy())
        
        # Remove current position from path (backtracking)
        path.pop()
    
    # Start DFS from each cell in the grid
    for row in range(rows):
        for col in range(cols):
            dfs(row, col, "", [], set())
    
    return found_words

def find_best_word(grid, dictionary_path="dictionary.txt"):
    # Load dictionary with absolute path
    import os
    if dictionary_path == "dictionary.txt":
        # Get the directory where this script is located and go up one level to spellcast-solver
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dictionary_path = os.path.join(script_dir, "dictionary.txt")
    words, prefix_set = load_dictionary(dictionary_path)
    
    # Find all valid words
    valid_words = find_words(grid, words, prefix_set)
    
    # If no valid words found
    if not valid_words:
        return None, 0, []
    
    # Sort by score (descending) and return the best one
    valid_words.sort(key=lambda x: x[1], reverse=True)
    
    return valid_words[0]

def format_path(path):
    if not path or len(path) < 2:
        return ""
    
    instructions = []
    
    # Add starting position
    start_row, start_col = path[0]
    instructions.append(f"Start at position ({start_row+1}, {start_col+1})")
    
    # Add movements
    for i in range(1, len(path)):
        prev_row, prev_col = path[i-1]
        curr_row, curr_col = path[i]
        
        # Determine direction
        row_diff = curr_row - prev_row
        col_diff = curr_col - prev_col
        
        # Convert to cardinal/intercardinal direction
        direction = ""
        if row_diff == -1 and col_diff == -1:
            direction = "Northwest"
        elif row_diff == -1 and col_diff == 0:
            direction = "North"
        elif row_diff == -1 and col_diff == 1:
            direction = "Northeast"
        elif row_diff == 0 and col_diff == -1:
            direction = "West"
        elif row_diff == 0 and col_diff == 1:
            direction = "East"
        elif row_diff == 1 and col_diff == -1:
            direction = "Southwest"
        elif row_diff == 1 and col_diff == 0:
            direction = "South"
        elif row_diff == 1 and col_diff == 1:
            direction = "Southeast"
            
        instructions.append(f"Move {direction} to ({curr_row+1}, {curr_col+1})")
    
    return "\n".join(instructions)

def display_grid_with_path(grid, path):
    path_set = set(path)
    display_lines = []
    
    # Create the top border
    display_lines.append("+" + "-" * (len(grid[0]) * 4 - 1) + "+")
    
    for row in range(len(grid)):
        # Build the row with letters and path indicators
        row_str = "|"
        for col in range(len(grid[0])):
            # Check if this position is in the path
            if (row, col) in path_set:
                # Find the position in the path to determine the sequence number
                pos = path.index((row, col))
                # Mark path positions with sequence numbers
                row_str += f" {grid[row][col]}{pos+1} "
            else:
                row_str += f" {grid[row][col]}  "
                
            if col < len(grid[0]) - 1:
                row_str += "|"
                
        row_str += "|"
        display_lines.append(row_str)
        
        # Add separator lines between rows
        if row < len(grid) - 1:
            display_lines.append("|" + "-" * (len(grid[0]) * 4 - 1) + "|")
    
    # Add bottom border
    display_lines.append("+" + "-" * (len(grid[0]) * 4 - 1) + "+")
    
    return "\n".join(display_lines)

def solve_grid(grid, dictionary_path="dictionary.txt"):
    # Validate grid
    if not grid or not grid[0]:
        return {"error": "Empty grid provided"}
    
    # Resolve dictionary path if using default
    import os
    if dictionary_path == "dictionary.txt":
        # Get the directory where this script is located and go up one level to spellcast-solver
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dictionary_path = os.path.join(script_dir, "dictionary.txt")
    
    # Find the best word
    word, score, path = find_best_word(grid, dictionary_path)
    
    if not word:
        return {"error": "No valid words found in the grid"}
    
    # Create the results
    results = {
        "word": word,
        "score": score,
        "path": path,
        "path_instructions": format_path(path),
        "grid_display": display_grid_with_path(grid, path)
    }
    
    return results



def solve_grid_main():
    grid = export_grid()

    results = solve_grid(grid)
    print(f"\nBest word found: {results['word']} (Score: {results['score']})")
    print("\nPath to follow:")
    print(results['path_instructions'])
    print("\nGrid with path:")
    print(results['grid_display'])