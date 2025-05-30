import numpy as np

class Opponent:
    def __init__(self, money, q_o, cost):
        self.q_o = q_o
        self.money = money
        self.cost = cost

    def produce(self):
        self.money -= self.cost * self.q_o
        return self.q_o

#demand function: p = 100 - Q
#TC_i = Costs[-1]*q_i

money = 1000
Costs = [50]
overall_production = 0
q_o = 0

year = 8
run = True
while run:
    print(f'Year {year}')
    if year == 9:
        print('Alert! A new competitor will enter the market next year!')
    if year == 10:
        print('Alert! A new competitor has entered the market!')
        newOpponent = Opponent(100, 40, 50)
    print(f'Money: {money}')
    print('demand function: p = 100 - Q')
    if year == 1:
        print(f'costs: {Costs[-1]}')
    else:
        print(f'your employees learnt something, costs are now {Costs[-1]}')
    
    q_i = int(input('Input how much to produce: '))
    if year > 9:
        Q = q_i + newOpponent.produce()
    else:
        Q = q_i

    overall_production += q_i
    p = max(100 - Q, 0)
    
    profit = q_i * p - Costs[-1] * q_i
    
    money += profit
    
    print(f'Profit: {profit}')
    if year > 9:
        print(f'money of opponent: {newOpponent.money}')
    
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
    print ('\n-----------------------------------\n')