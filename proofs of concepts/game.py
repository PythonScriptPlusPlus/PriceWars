import numpy as np

class Company:
    def __init__(self, money, q, cost):
        self.q = q
        self.money = money
        self.cost = cost
        self.overall_production = 0

    def produce(self):
        self.money -= self.cost[-1] * self.q
        return self.q

#demand function: p = 100 - Q
#TC_i = Costs[-1]*q_i

Player = Company(1000, 0, [50])

# money = 1000
# Costs = [50]
# overall_production = 0
# q_o = 0

year = 8
run = True
while run:
    print(f'Year {year}')
    if year == 9:
        print('Alert! A new competitor will enter the market next year!')
    if year == 10:
        print('Alert! A new competitor has entered the market!')
        Opponent = Company(100, 40, 50)
    print(f'Money: {Player.money}')
    print('demand function: p = 100 - Q')
    if year == 1:
        print(f'costs: {Player.cost[-1]}')
    else:
        print(f'your employees learnt something, costs are now {Player.cost[-1]}')
    
    Player.q = int(input('Input how much to produce: '))
    if year > 9:
        Q = Player.q + Opponent.produce()
    else:
        Q = Player.q

    Player.overall_production += Player.q
    p = max(100 - Q, 0)
    
    profit = Player.q * p - Player.cost[-1] * Player.q
    
    Player.money += profit
    
    print(f'Profit: {profit}')
    if year > 9:
        print(f'money of opponent: {Opponent.money}')
    
    if Player.money <= 0:
        print('You are out of money!')
        run = False
    
    elif input('Continue? (y/n): ').lower() != 'y':
        run = False
    
    alpha = -0.05
    ut = np.random.normal(0, 0.025)
    newCost = Player.cost[0] * Player.overall_production**alpha * np.e**ut
    Player.cost.append(round(newCost, 2))

    year += 1
    print ('\n-----------------------------------\n')