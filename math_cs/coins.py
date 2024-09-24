
# This method only works for the very simple case.. 
def simple_change_for_coins(amount):
    coins = []
    while amount > 0:
        if amount % 7 == 0:
            coins.extend([7 for _ in range(amount // 7)])
            amount = 0
        elif amount >= 5:
            coins.append(5)
            amount -= 5
        else: 
            return []
    return coins



print(simple_change_for_coins(23))
print(simple_change_for_coins(24))
print(simple_change_for_coins(33))
