import numpy as np
import math

def solve_equation(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        print('no work',b**2, 4*a*c, discriminant)
        return None  # No real roots
    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
    root2 = (-b - math.sqrt(discriminant)) / (2 * a)
    print(f"Roots: {root1}, {root2}")
    return (root1, root2)

class Company:
    def __init__(self, money, q, cost, period=1, demand=100, opponent=False, additional_cost=0, one_time_cost=0):
        self.q = q
        self.money = money
        self.cost = cost
        self.overall_production = 0
        self.period = period
        self.health = 100
        self.demand = demand
        self.opponent = opponent
        self.additional_cost = additional_cost
        self.one_time_cost = one_time_cost

    # demand function: p = 100 - Q
    def produce(self, enemy=None):
        is_enemy_defeated = False
        if not enemy:
            profit = (self.demand - self.q) * self.q - self.cost[-1] * self.q - self.additional_cost - self.one_time_cost
            self.one_time_cost = 0
            self.money += profit
            self.money = round(self.money, 2)
            self.period += 1
            self.overall_production += self.q

            optimal_q = (self.demand - self.cost[-1])/2
            optimal_profit = (self.demand - optimal_q) * optimal_q - self.cost[-1] * optimal_q - self.additional_cost
            exitLog = ''
        else:
            if enemy.one_time_cost >= enemy.money:
                exitLog = '<span style="color:#c22955">Конкурирующая компания не смогла войти на рынок, из-за высокой стоимости вхождения</span>\n'
                is_enemy_defeated = True
                self.produce()
                return (exitLog, is_enemy_defeated)
            enemy.q = max(min((self.demand - self.q-enemy.cost[-1])/2, (enemy.money-enemy.one_time_cost-enemy.additional_cost)/enemy.cost[-1]), 0)
            enemy.period += 1
            profit = (self.demand - self.q - enemy.q) * self.q - self.cost[-1] * self.q - self.additional_cost - self.one_time_cost
            self.money += profit
            self.money = round(self.money, 2)
            self.period += 1
            self.overall_production += self.q

            enemy_profit = (self.demand - self.q - enemy.q) * enemy.q - enemy.cost[-1] * enemy.q - enemy.additional_cost - enemy.one_time_cost
            enemy.one_time_cost = 0
            enemy.money += enemy_profit

            if enemy.q == 0 or enemy_profit <= 0:
                enemy.health -= 34
                if enemy.health > 0:
                    exitLog = '<span style="color:#c22955">Новая фирма на рынке терпит убытки, и 34% процента изначальных инвесторов отворачиваются от неё</span>\n'
                else:
                    exitLog = '<span style="color:#c22955">После серии неудачных периодов новой фирме приходится объявить банкротство и покинуть рынок</span>\n'
            else:
                exitLog = f'<span style="color:#8a209e">Новая фирма на рынке получает прибыль в размере {enemy_profit} и укрепляет свои позиции на рынке</span>\n'

            optimal_q = min(solve_equation(1, 2*(self.cost[-1]-self.demand), self.demand**2 + self.cost[-1]**2 - 4*enemy.additional_cost - 2*self.cost[-1]*self.demand))
            optimal_profit = (self.demand - optimal_q) * optimal_q - self.cost[-1] * optimal_q

            print(f"Your profit: {profit}, Your money: {self.money}, your optimal q: {optimal_q}, your optimal profit: {optimal_profit}")
            print(f"Enemy profit: {enemy_profit}, Enemy money: {enemy.money}, Enemy q: {enemy.q}, Enemy period: {enemy.period}, enemy cost: {enemy.cost[-1]}")
            print(f"Enemy TC: {enemy.additional_cost} + {enemy.cost[-1]} * q")

            self.health -= 10 * (enemy.period/4)**3
            if 10 * (enemy.period/4)**3 > profit/optimal_profit * 25:
                exitLog += '<span style="color:#c22955">Конкурирующая компания достаточно долго была на рынке, и ваши инвесторы начали присматриваться к ней</span>\n'
            
            if enemy.health <= 0:
                print('Enemy has been defeated')
                is_enemy_defeated = True
        if profit <= 0:
            self.health -= 25
        else:
            print(f'supposed to heal, optimal_q: {optimal_q}, optimal profit: {optimal_profit}, ratio: {profit/optimal_profit}')
            self.health = round(min(100, self.health + profit/optimal_profit * 25))


        alpha = -0.05
        ut = np.random.normal(0, 0.025)
        newCost = self.cost[0] * self.overall_production**alpha * np.e**ut
        self.cost.append(round(newCost, 2))
        return (exitLog, is_enemy_defeated)