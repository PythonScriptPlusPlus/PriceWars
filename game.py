import numpy as np

class Company:
    def __init__(self, money, q, cost, period=1, demand=100):
        self.q = q
        self.money = money
        self.cost = cost
        self.overall_production = 0
        self.period = period
        self.health = 100
        self.demand = demand

    # demand function: p = 100 - Q
    def produce(self):
        profit = (self.demand - self.q) * self.q - self.cost[-1] * self.q
        self.money += profit
        self.money = round(self.money, 2)
        self.period += 1
        self.overall_production += self.q

        optimal_q = (self.demand - self.cost[-1])/2
        optimal_profit = (self.demand - optimal_q) * optimal_q - self.cost[-1] * optimal_q
        if profit <= 0:
            self.health -= 25
        else:
            self.health = round(min(100, self.health + profit/optimal_profit * 25))


        alpha = -0.05
        ut = np.random.normal(0, 0.025)
        newCost = self.cost[0] * self.overall_production**alpha * np.e**ut
        self.cost.append(round(newCost, 2))
        return self.q
