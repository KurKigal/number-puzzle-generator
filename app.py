from flask import Flask, render_template, jsonify, request
import random
import json
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
from copy import deepcopy

app = Flask(__name__)

@dataclass
class NumberInfo:
    value: str
    length: int
    start_row: int
    start_col: int
    direction: str  # 'horizontal' or 'vertical'
    
class NumberPuzzleGenerator:
    def __init__(self):
        self.grid_size = 15
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.black_cells = set()
    
    def generate_black_cells(self):
        """Place initial black cells randomly (fewer at first, more will be added later)"""
        total_cells = self.grid_size * self.grid_size
        # Start with fewer black cells initially
        initial_black_count = random.randint(int(total_cells * 0.08), int(total_cells * 0.12))
        
        while len(self.black_cells) < initial_black_count:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.black_cells.add((row, col))
    
    def fill_with_random_digits(self):
        """Fill all empty cells with random digits"""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) not in self.black_cells:
                    # Use 0 digit less frequently
                    if random.random() < 0.15:  # 15% chance for 0
                        self.grid[row][col] = 0
                    else:
                        self.grid[row][col] = random.randint(1, 9)  # 1-9 range
    
    def break_repetitive_patterns(self):
        """Break overly regular numbers (8888, 777, etc.)"""
        
        # Horizontal check
        for row in range(self.grid_size):
            consecutive_count = 1
            current_digit = None
            
            for col in range(self.grid_size):
                if (row, col) in self.black_cells:
                    consecutive_count = 1
                    current_digit = None
                    continue
                
                if current_digit == self.grid[row][col]:
                    consecutive_count += 1
                    # If more than 3 same digits side by side, change it
                    if consecutive_count > 3:
                        self.grid[row][col] = random.randint(0, 9)
                        while self.grid[row][col] == current_digit:
                            self.grid[row][col] = random.randint(0, 9)
                        current_digit = self.grid[row][col]
                        consecutive_count = 1
                else:
                    current_digit = self.grid[row][col]
                    consecutive_count = 1
        
        # Vertical check
        for col in range(self.grid_size):
            consecutive_count = 1
            current_digit = None
            
            for row in range(self.grid_size):
                if (row, col) in self.black_cells:
                    consecutive_count = 1
                    current_digit = None
                    continue
                
                if current_digit == self.grid[row][col]:
                    consecutive_count += 1
                    # If more than 3 same digits vertically, change it
                    if consecutive_count > 3:
                        self.grid[row][col] = random.randint(0, 9)
                        while self.grid[row][col] == current_digit:
                            self.grid[row][col] = random.randint(0, 9)
                        current_digit = self.grid[row][col]
                        consecutive_count = 1
                else:
                    current_digit = self.grid[row][col]
                    consecutive_count = 1
    
    def add_separating_black_cells(self):
        """Add strategic black cells to separate numbers"""
        sequences = self.find_all_sequences()
        
        # Split very long sequences (7+ digits)
        for seq in sequences:
            if len(seq) > 7:
                # Split near the middle
                break_point = len(seq) // 2 + random.randint(-1, 1)
                if 0 < break_point < len(seq):
                    break_row, break_col = seq[break_point]
                    self.black_cells.add((break_row, break_col))
        
        # IMPORTANT: Separate adjacent numbers
        self.separate_adjacent_numbers()
        
        # Add some random black cells for variety
        filled_cells = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) not in self.black_cells:
                    filled_cells.append((row, col))
        
        # Add 5-10% additional random black cells
        additional_black_count = random.randint(len(filled_cells) // 20, len(filled_cells) // 10)
        additional_blacks = random.sample(filled_cells, additional_black_count)
        
        for row, col in additional_blacks:
            self.black_cells.add((row, col))
    
    def separate_adjacent_numbers(self):
        """Add black cells to separate adjacent numbers"""
        sequences = self.find_all_sequences()
        
        # Add black cells after each 3-7 digit sequence
        for seq in sequences:
            if 3 <= len(seq) <= 7:
                last_row, last_col = seq[-1]
                
                # If horizontal sequence (same row)
                if len(seq) > 1 and seq[0][0] == seq[1][0]:  # Horizontal
                    # Add black cell to the right
                    next_col = last_col + 1
                    if (next_col < self.grid_size and 
                        (last_row, next_col) not in self.black_cells and
                        random.random() < 0.4):  # 40% chance
                        self.black_cells.add((last_row, next_col))
                
                # If vertical sequence (same column)
                elif len(seq) > 1 and seq[0][1] == seq[1][1]:  # Vertical
                    # Add black cell below
                    next_row = last_row + 1
                    if (next_row < self.grid_size and 
                        (next_row, last_col) not in self.black_cells and
                        random.random() < 0.4):  # 40% chance
                        self.black_cells.add((next_row, last_col))
        
        # Additionally: split in the middle of 4+ digit sequences
        for seq in sequences:
            if len(seq) >= 4:
                # Add separator every 3-4 digits
                for i in range(3, len(seq), random.randint(3, 5)):
                    if i < len(seq):
                        break_row, break_col = seq[i]
                        if random.random() < 0.3:  # 30% chance
                            self.black_cells.add((break_row, break_col))
    
    def find_all_sequences(self) -> List[List[Tuple[int, int]]]:
        """Find all continuous sequences in the grid"""
        sequences = []
        
        # Horizontal sequences
        for row in range(self.grid_size):
            current_seq = []
            for col in range(self.grid_size):
                if (row, col) in self.black_cells:
                    # Black cell found, save current sequence
                    if len(current_seq) >= 2:
                        sequences.append(current_seq)
                    current_seq = []
                else:
                    current_seq.append((row, col))
            
            # Save remaining sequence at end of row
            if len(current_seq) >= 2:
                sequences.append(current_seq)
        
        # Vertical sequences
        for col in range(self.grid_size):
            current_seq = []
            for row in range(self.grid_size):
                if (row, col) in self.black_cells:
                    # Black cell found, save current sequence
                    if len(current_seq) >= 2:
                        sequences.append(current_seq)
                    current_seq = []
                else:
                    current_seq.append((row, col))
            
            # Save remaining sequence at end of column
            if len(current_seq) >= 2:
                sequences.append(current_seq)
        
        return sequences
    
    def fix_leading_zeros(self):
        """Fix sequences starting with 0"""
        sequences = self.find_continuous_sequences()
        
        for seq in sequences:
            if len(seq) >= 2:
                start_row, start_col = seq[0]
                # If sequence starts with 0, make first digit 1-9
                if self.grid[start_row][start_col] == 0:
                    self.grid[start_row][start_col] = random.randint(1, 9)
    
    def ensure_all_cells_covered(self):
        """Ensure all white cells are part of a number"""
        sequences = self.find_continuous_sequences()
        covered_cells = set()
        
        # Mark cells covered by existing sequences
        for seq in sequences:
            if len(seq) >= 2:  # At least 2-digit sequences
                for cell in seq:
                    covered_cells.add(cell)
        
        # Find uncovered cells
        uncovered_cells = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) not in self.black_cells and (row, col) not in covered_cells:
                    uncovered_cells.append((row, col))
        
        # Fix uncovered cells
        for row, col in uncovered_cells:
            self.fix_uncovered_cell(row, col)
    
    def fix_uncovered_cell(self, row: int, col: int):
        """Fix uncovered cell by expanding neighbors"""
        # Try horizontal expansion
        horizontal_extended = False
        
        # Expand left
        if col > 0 and (row, col - 1) not in self.black_cells:
            # Include left neighbor too
            if col > 1 and (row, col - 2) not in self.black_cells:
                # At least 3-digit horizontal number created
                horizontal_extended = True
            elif col < self.grid_size - 1 and (row, col + 1) not in self.black_cells:
                # Also expand right, 3-digit horizontal number
                horizontal_extended = True
        
        # Expand right
        elif col < self.grid_size - 1 and (row, col + 1) not in self.black_cells:
            if col < self.grid_size - 2 and (row, col + 2) not in self.black_cells:
                # At least 3-digit horizontal number created
                horizontal_extended = True
        
        # Try vertical expansion (if horizontal failed)
        if not horizontal_extended:
            # Expand up
            if row > 0 and (row - 1, col) not in self.black_cells:
                if row > 1 and (row - 2, col) not in self.black_cells:
                    # At least 3-digit vertical number created
                    pass
                elif row < self.grid_size - 1 and (row + 1, col) not in self.black_cells:
                    # Also expand down, 3-digit vertical number
                    pass
            
            # Expand down
            elif row < self.grid_size - 1 and (row + 1, col) not in self.black_cells:
                if row < self.grid_size - 2 and (row + 2, col) not in self.black_cells:
                    # At least 3-digit vertical number created
                    pass
            
            # If no expansion possible, convert neighbor black cell to white
            else:
                self.convert_neighbor_to_white(row, col)
    
    def convert_neighbor_to_white(self, row: int, col: int):
        """Convert neighbor black cell to white"""
        neighbors = [
            (row - 1, col), (row + 1, col),  # top, bottom
            (row, col - 1), (row, col + 1)   # left, right
        ]
        
        # Find a black neighbor and convert to white
        for nr, nc in neighbors:
            if (0 <= nr < self.grid_size and 0 <= nc < self.grid_size and 
                (nr, nc) in self.black_cells):
                
                # Remove this black cell and give it a random digit
                self.black_cells.remove((nr, nc))
                self.grid[nr][nc] = random.randint(0, 9)
                break
    
    def find_continuous_sequences(self) -> List[List[Tuple[int, int]]]:
        """Find continuous number sequences in the grid"""
        sequences = []
        
        # Horizontal sequences
        for row in range(self.grid_size):
            current_seq = []
            for col in range(self.grid_size):
                if (row, col) in self.black_cells:
                    # Black cell found, save current sequence
                    if len(current_seq) >= 2:
                        sequences.append(current_seq)
                    current_seq = []
                else:
                    current_seq.append((row, col))
            
            # Save remaining sequence at end of row
            if len(current_seq) >= 2:
                sequences.append(current_seq)
        
        # Vertical sequences
        for col in range(self.grid_size):
            current_seq = []
            for row in range(self.grid_size):
                if (row, col) in self.black_cells:
                    # Black cell found, save current sequence
                    if len(current_seq) >= 2:
                        sequences.append(current_seq)
                    current_seq = []
                else:
                    current_seq.append((row, col))
            
            # Save remaining sequence at end of column
            if len(current_seq) >= 2:
                sequences.append(current_seq)
        
        return sequences
    
    def extract_numbers_from_grid(self) -> Dict:
        """Extract numbers from grid and group by digit count"""
        sequences = self.find_continuous_sequences()
        numbers_by_length = {2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        
        for seq in sequences:
            # Accept 2-7 digit numbers
            if 2 <= len(seq) <= 7:
                number_str = ""
                for row, col in seq:
                    number_str += str(self.grid[row][col])
                
                # Skip numbers starting with 0 (not real numbers)
                if number_str.startswith('0') and len(number_str) > 1:
                    continue
                
                # Skip 7+ digit numbers (too long)
                if len(number_str) > 7:
                    continue
                
                # Add only unique numbers
                if len(number_str) in numbers_by_length:
                    if number_str not in numbers_by_length[len(number_str)]:
                        numbers_by_length[len(number_str)].append(number_str)
        
        # If too many numbers in category, randomly select
        for length in numbers_by_length:
            if len(numbers_by_length[length]) > 15:
                numbers_by_length[length] = random.sample(numbers_by_length[length], 15)
        
        return numbers_by_length
    
    def create_puzzle_grid(self, hint_cells) -> List[List[str]]:
        """Create cleaned grid for player"""
        puzzle_grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Fill hint cells
        hint_positions = {(row, col) for row, col, val in hint_cells}
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) in self.black_cells:
                    puzzle_grid[row][col] = "BLACK"  # Black cell marker
                elif (row, col) in hint_positions:
                    # Find hint value
                    hint_value = next(val for r, c, val in hint_cells if r == row and c == col)
                    puzzle_grid[row][col] = str(hint_value)
                else:
                    puzzle_grid[row][col] = ""  # Empty cell
        
        return puzzle_grid
    
    def select_hint_cells(self) -> List[Tuple[int, int, int]]:
        """Select hint cells"""
        hint_count = random.randint(5, 8)
        hints = []
        
        # Select randomly from all filled cells (including 0)
        filled_cells = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if (row, col) not in self.black_cells:
                    # Include all digits including 0
                    filled_cells.append((row, col, self.grid[row][col]))
        
        hints = random.sample(filled_cells, min(hint_count, len(filled_cells)))
        return hints
    
    def generate_puzzle(self) -> Dict:
        """Generate puzzle using new algorithm"""
        
        # 1. Generate black cells
        self.generate_black_cells()
        
        # 2. Fill all empty cells with random digits
        self.fill_with_random_digits()
        
        # 3. Break overly regular numbers (8888, 777, etc.)
        self.break_repetitive_patterns()
        
        # 4. Add separating black cells
        self.add_separating_black_cells()
        
        # 5. Fix sequences starting with 0
        self.fix_leading_zeros()
        
        # 6. Ensure all white cells are part of a number
        self.ensure_all_cells_covered()
        
        # 7. Extract and list numbers
        extracted_numbers = self.extract_numbers_from_grid()
        
        # 8. Select hint cells
        hint_cells = self.select_hint_cells()
        
        # 9. Clean game area (only hints remain)
        puzzle_grid = self.create_puzzle_grid(hint_cells)
        
        return {
            'solution_grid': self.grid,  # Complete solution
            'puzzle_grid': puzzle_grid,   # Cleaned grid for player
            'black_cells': list(self.black_cells),
            'available_numbers': extracted_numbers,
            'hint_cells': hint_cells,
            'success': True
        }

# Flask routes
generator = NumberPuzzleGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_puzzle():
    """Generate new puzzle"""
    global generator
    generator = NumberPuzzleGenerator()
    result = generator.generate_puzzle()
    return jsonify(result)

@app.route('/api/puzzle/current')
def get_current_puzzle():
    """Return current puzzle"""
    if not hasattr(generator, 'grid') or not any(any(row) for row in generator.grid):
        return jsonify({'success': False, 'error': 'No puzzle generated yet'})
    
    return jsonify({
        'grid': generator.grid,
        'black_cells': list(generator.black_cells),
        'success': True
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)