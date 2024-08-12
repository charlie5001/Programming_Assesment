coins = [100, 20, 50, 10, 2, 5]

coins.sort(reverse=True)

k = 3

total_cost = 0
i = 0

while i < len(coins):
    total_cost += coins[i]  
    i += (k + 1)     

print(total_cost)