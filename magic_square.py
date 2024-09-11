

import itertools
import sys


def is_magic_square(square):
    # given a two dimensions list, return True if it is a magic square
    n = len(square)
    
    # Calculate the sum of the first row
    target_sum = sum(square[0])
    
    # Check if the sum of each row is equal to the target sum
    for row in square:
        if sum(row) != target_sum:
            return False
    
    # Check if the sum of each column is equal to the target sum
    for col in range(n):
        col_sum = sum(row[col] for row in square)
        if col_sum != target_sum:
            return False
    
    # Check if the sum of the main diagonal is equal to the target sum
    main_diag_sum = sum(square[i][i] for i in range(n))
    if main_diag_sum != target_sum:
        return False
    
    # Check if the sum of the secondary diagonal is equal to the target sum
    sec_diag_sum = sum(square[i][n-i-1] for i in range(n))
    if sec_diag_sum != target_sum:
        return False
    
    # If all checks pass, the square is a magic square
    return True
    
def test_is_magic_square():
    square = [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]
    ]
    print(is_magic_square(square))  # True
    
    square = [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 3]
    ]
    print(is_magic_square(square))  # False
    

def find_squares(dimension):
    # given a dimension, return all magic squares of that dimension
    # Generate all possible permutations of numbers from 1 to dimension^2
    numbers = list(range(1, dimension**2 + 1))
    permutations = itertools.permutations(numbers)
    
    print('done generating permutations')
    # Filter permutations to only include those that form magic squares
    magic_squares = []
    
    for perm in permutations:
        square = [list(perm[i:i+dimension]) for i in range(0, dimension**2, dimension)]
        if is_magic_square(square):
            magic_squares.append(square)
    
    return magic_squares

def pretty_print(square):
    max_num_length = len(str(max(max(row) for row in square)))  # Get the length of the longest number in the square
    
    for row in square:
        for num in row:
            # Calculate the number of spaces needed to align the number
            num_spaces = max_num_length - len(str(num))
            
            # Print the number with the appropriate number of spaces
            print(' ' * num_spaces + str(num), end=' ')
        
        print()  # Move to the next row
    
    print()  # Add an empty line after printing the square

def find_squares_and_print(dimension):
    squares = find_squares(dimension)
    for square in squares:
        pretty_print(square)
    print(f'found {len(squares)} magic squares') 


if __name__ == '__main__':
    #find_squares_and_print(3)
    #test_find_squares()
    # get dimension from user as argument
    if len(sys.argv) != 2:
        print("Usage: python magic_square.py <dimension>")
        sys.exit(1)

    dimension = int(sys.argv[1])
    find_squares_and_print(dimension)

    
