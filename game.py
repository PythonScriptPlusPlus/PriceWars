import numpy as np

class Company:
    def __init__(self, money, q, cost, period=1):
        self.q = q
        self.money = money
        self.cost = cost
        self.overall_production = 0
        self.period = period

    # demand function: p = 100 - Q
    def produce(self):
        self.money = self.money - self.cost[-1] * self.q + (100 - self.q) * self.q
        self.period += 1
        self.overall_production += self.q

        alpha = -0.05
        ut = np.random.normal(0, 0.025)
        newCost = self.cost[0] * self.overall_production**alpha * np.e**ut
        self.cost.append(round(newCost, 2))
        return self.q
