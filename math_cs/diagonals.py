


# check how many diagonals can fit in a square matrix. 


# Helped function to avoid all boundary checks for row and col. 
#  Return true if the value is present at mat[row][col]. 
#  If row and col are outside the bounds, return False 
def is_value_present(mat, row, col, value):
    if row < 0 or row >= len(mat) or col < 0 or col >= len(mat[0]):
        return False
    return mat[row][col] == value

def print_matrix(mat):
    for row in mat:
        print(' '.join(row))
    print()

def recurse(mat, row, col, count, max_count):
    n = len(mat)
    if row >= n:        # we have reached the end
        if count > max_count:
            print(f'Max count = {count}\n')
            print_matrix(mat)
            max_count = count
        return max_count
    if col >= n:
        #print(f'Row {row} is done.. count is {count}')
        return recurse(mat, row + 1, 0, count, max_count)
    
    # current cell MUST be empty
    assert mat[row][col] == ' '

    # Check if we can add a \ diagonal
    if (is_value_present(mat, row - 1, col - 1, '\\') or  
        is_value_present(mat, row - 1, col    , '/') or  
        is_value_present(mat, row    , col - 1, '/')):
        #is_value_present(mat, row    , col - 1, '/') or  
        #is_value_present(mat, row    , col + 1, '/') or  
        #is_value_present(mat, row + 1, col    , '/') or  
        #is_value_present(mat, row + 1, col + 1, '\\')): 
        pass  # can not place a diagonal here
    else:
        mat[row][col] = '\\'
        max_count = recurse(mat, row, col + 1, count + 1, max_count)
        mat[row][col] = ' '
    
    # Check if we can add a / diagonal
    if (is_value_present(mat, row - 1, col    , '\\') or  
        is_value_present(mat, row - 1, col + 1, '/') or  
        is_value_present(mat, row    , col - 1, '\\')):
        #is_value_present(mat, row    , col - 1, '\\') or  
        #is_value_present(mat, row    , col + 1, '\\') or  
        #is_value_present(mat, row + 1, col - 1, '/') or  
        #is_value_present(mat, row + 1, col    , '\\')): 
        pass  # can not place a diagonal here
    else:
        mat[row][col] = '/'
        max_count = recurse(mat, row, col + 1, count + 1, max_count)
        mat[row][col] = ' '
    
    # place a blank space and continue
    max_count = recurse(mat, row, col + 1, count, max_count)
    return max_count


def diagonals(n):
    mat = [[' ' for _ in range(n)] for _ in range(n)]
    max_count = recurse(mat, 0, 0, 0, 0)


diagonals(3)
diagonals(5)