import numpy as np

class Company:
    def __init__(self, money, q, cost, period=1, demand=100, opponent=False, additional_cost=0):
        self.q = q
        self.money = money
        self.cost = cost
        self.overall_production = 0
        self.period = period
        self.health = 100
        self.demand = demand
        self.opponent = opponent
        self.additional_cost = additional_cost

    # demand function: p = 100 - Q
    def produce(self, enemy=None):
        if not enemy:
            profit = (self.demand - self.q) * self.q - self.cost[-1] * self.q
            self.money += profit
            self.money = round(self.money, 2)
            self.period += 1
            self.overall_production += self.q

            optimal_q = (self.demand - self.cost[-1])/2
            optimal_profit = (self.demand - optimal_q) * optimal_q - self.cost[-1] * optimal_q
        else:
            enemy.q = (self.demand - self.q)/2
            profit = (self.demand - self.q - enemy.q) * self.q - self.cost[-1] * self.q - self.additional_cost
            self.money += profit
            self.money = round(self.money, 2)
            self.period += 1
            self.overall_production += self.q

            enemy_profit = (self.demand - self.q - enemy.q) * enemy.q - enemy.cost[-1] * enemy.q - enemy.additional_cost
            enemy.money += enemy_profit

            print(f"Your profit: {profit}, Your money: {self.money}")
            print(f"Enemy profit: {enemy_profit}, Enemy money: {enemy.money}")
        if profit <= 0:
            self.health -= 25
        else:
            self.health = round(min(100, self.health + profit/optimal_profit * 25))


        alpha = -0.05
        ut = np.random.normal(0, 0.025)
        newCost = self.cost[0] * self.overall_production**alpha * np.e**ut
        self.cost.append(round(newCost, 2))
        return self.q
