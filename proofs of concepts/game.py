import numpy as np

#demand function: p = 100 - Q
#TC_i = Costs[-1]*q_i

money = 1000
Costs = [50]
overall_production = 0

year = 1
run = True
while run:
    print(f'Year {year}')
    if year == 9:
        print('Alert! A new competitor will enter the market next year!')
    print(f'Money: {money}')
    print('demand function: p = 100 - Q')
    if year == 1:
        print(f'costs: {Costs[-1]}')
    else:
        print(f'your employees learnt something, costs are now {Costs[-1]}')
    
    q_i = int(input('Input how much to produce: '))
    
    Q = q_i
    overall_production += q_i
    p = max(100 - Q, 0)
    
    profit = q_i * p - Costs[-1] * q_i
    
    money += profit
    
    print(f'Profit: {profit}')
    
    if money <= 0:
        print('You are out of money!')
        run = False
    
    if input('Continue? (y/n): ').lower() != 'y':
        run = False
    
    alpha = -0.05
    ut = np.random.normal(0, 0.025)
    newCost = Costs[0] * overall_production**alpha * np.e**ut
    Costs.append(round(newCost, 2))

    year += 1