
# this function checks if a number is prime
def is_prime(n):    
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True 


for i in range(1, 1000):
    val = i*i + i + 41
    if not is_prime(val):
        print(f"{val} is not prime")
        break
