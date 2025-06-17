import numpy as np
import math

# Функция для решения квадратного уравнения ax^2 + bx + c = 0
def solve_equation(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None  # No real roots
    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
    root2 = (-b - math.sqrt(discriminant)) / (2 * a)
    return (root1, root2)

# Класс Company представляет компанию с её финансами, производственными затратами и периодами
# Этот класс используется и игроком, и противником
class Company:
    def __init__(self, money, q, cost, period=1, demand=100, opponent=False, additional_cost=0, one_time_cost=0):
        self.q = q # Количество продукции, производимое компанией
        self.money = money # Количество денег у компании
        self.cost = cost # Стоимость производства компании
        self.overall_production = 0 # Общее количество произведённой продукции
        self.period = period # Количество периодов, которое компания существует
        self.health = 100 # Здоровье компании, которое уменьшается при убытках. Репрезентует терпение инвесторов
        self.demand = demand # Функция спроса, которая определяет цену в зависимости от количества продукции
        self.opponent = opponent # Флаг, указывающий, является ли компания противником
        self.additional_cost = additional_cost # Дополнительные затраты, которые компания несёт при производстве
        self.one_time_cost = one_time_cost # Одноразовые затраты, которые компания несёт при входе на рынок

    # demand function: p = 100 - Q
    def produce(self, enemy=None):
        is_enemy_defeated = False
        if not enemy: # Производство при отсутствии противника на рынке
            profit = (self.demand - self.q) * self.q - self.cost[-1] * self.q - self.additional_cost - self.one_time_cost
            self.one_time_cost = 0
            self.money += profit
            self.money = round(self.money, 2)
            self.period += 1
            self.overall_production += self.q

            optimal_q = (self.demand - self.cost[-1])/2 # Оптимальное количество продукции, которое нужно произвести для максимизации прибыли
            optimal_profit = (self.demand - optimal_q) * optimal_q - self.cost[-1] * optimal_q - self.additional_cost # Оптимальная прибыль, которую можно получить при оптимальном количестве продукции. Используется для восстановления здоровья компании
            exitLog = '' # Дополнительная информация о производстве, которая будет отображаться в интерфейсе. Испольуется, когда есть противник на рынке
        else:
            if enemy.one_time_cost >= enemy.money: # Если противник не может войти на рынок из-за нехватки денег
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

            # Противник теряет убытки, если его прибыль меньше или равна нулю
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


            self.health -= 10 * (enemy.period/4)**3
            if 10 * (enemy.period/4)**3 > profit/optimal_profit * 25: # Игрок теряет здоровье, если оппонент присутствует на рынке достаточно долго и/или игрок не делает оптимальные действия
                exitLog += '<span style="color:#c22955">Конкурирующая компания достаточно долго была на рынке, и ваши инвесторы начали присматриваться к ней</span>\n'
            
            if enemy.health <= 0:
                is_enemy_defeated = True
        if profit <= 0:
            self.health -= 25
        else:
            self.health = round(min(100, self.health + profit/optimal_profit * 25))

        # Формула с производства Генри Форда. Уменьшает затраты на производство, всзязи с обучением сотрудников и оптимизацией процессов
        alpha = -0.05
        ut = np.random.normal(0, 0.025)
        newCost = self.cost[0] * self.overall_production**alpha * np.e**ut
        self.cost.append(round(newCost, 2))
        return (exitLog, is_enemy_defeated)