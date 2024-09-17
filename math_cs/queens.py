

import itertools as it

def brute_force_n_queens(n):
    def is_valid(perm):
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if abs(perm[i] - perm[j]) == abs(i - j):
                    return False
        return True 

    # iterate through all permutations of 8 
    for perm in it.permutations(range(n)):
        # check if the permutation is a solution
        if is_valid(perm):
            print(perm)
            break
        


def new_entry_is_valid(perm):
    i = len(perm) - 1
    for j in range(i):
        if abs(perm[i] - perm[j]) == abs(i - j):
            return False
    return True 

def backtrack_queens(n, perms, count = 0):
    if len(perms) == n:
        print(perms)
        return count + 1
    
    for i in range(n):
        if i not in perms:
            perms.append(i)
            if new_entry_is_valid(perms):
                count = backtrack_queens(n, perms, count)
            perms.pop()
    return count

brute_force_n_queens(8)
#brute_force_n_queens(20)
print('count = ', backtrack_queens(4, [], 0))
print('count = ', backtrack_queens(8, [], 0))
#print('count = ', backtrack_queens(20, [], 0))