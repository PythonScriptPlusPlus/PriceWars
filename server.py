import random
import traceback
import numpy as np
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from game import Company

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "http://5.180.174.128",
    "http://5.180.174.128:8080"
]}})
# Создаёт начальные значения для игрока и противника
Player = Company(1000000, 0, [50])  # Создаём игрока с начальными деньгами, количеством продукции и стоимостью
Opponent = None # Изначально противник не существует
Opponent_window = 0 # Счётчик периодов, между победой над противником и его появлением
demand_constant = 100 # Начальная величина спроса
base_cost = 50 # Начальная стоимость производства
entry_cost = 0 # Стоимость входа на рынок для противника
enemy_modifier = 1 # Модификатор для противника, увеличивается при победе над ним
property_price = 1000 # Начальная цена собственности, которую игрок может купить
player_plots = [] # Список собственности игрока, который будет обновляться при покупке
opponent_adcost = 50 # Начальная стоимость производства для противника, которая будет увеличиваться при покупке собственности

log = 'Игра запущена. Выберите количество продукции для производства.' # История действий игрока, которая будет отображаться в Vue-приложении

# Передаём начальные значения для игрока в Vue-приложение
@app.route('/data', methods=['GET'])
def get_data():
    data = {
        'health': Player.health,
        'period': Player.period,
        'money': Player.money,
        'demand': 100,
        'costs': Player.cost[-1],
        'overallProduction': Player.overall_production,
        'long_text': log,
        'property_price': property_price,
        'playersPlots': player_plots,
    }
    return jsonify(data)

# Производит продукцию игрока и противника, если он существует
@app.route('/production', methods=['POST'])
def receive_production():
    global log, Opponent, Opponent_window, Player, demand_constant, enemy_modifier, property_price
    Player.demand = demand_constant
    is_enemy_defeated = False
    data = request.get_json()
    production_amount = data.get('productionAmount')
    long_text = data.get('longText')
    try:
        Player.q = int(production_amount)
        if Player.period < 10:
            line, is_enemy_defeated = Player.produce() # Производим продукцию игрока без противника
        else:
            if Player.period == 10 or (Opponent_window == -1 and Player.period > 2):
                Opponent = Company(1000*enemy_modifier, 0, [base_cost], period=1, demand=demand_constant, opponent=True, additional_cost=opponent_adcost, one_time_cost=entry_cost)

            line, is_enemy_defeated = Player.produce(Opponent) # Производим продукцию игрока с противником
            
        # Вывод информации о производстве
        long_text = 'В период <span style="color:skyblue">{}</span> ваша компания произвела <span style="color:#ffc55b">{}</span> единиц продукции'.format(Player.period-1, Player.q) + '\n' + long_text
        long_text = 'В период <span style="color:skyblue">{}</span> прибыль от произведённой продукции составила <span style="color:#39f139">{}</span> рублей'.format(Player.period-1,round(Player.q * (Player.demand - Player.q) - Player.cost[-2] * Player.q - Player.additional_cost,2)) + '\n' + long_text
        if is_enemy_defeated: # Проверяем, победил ли игрок противника
            long_text = '<span style="color:green">Вы победили конкурента!</span>' + '\n' + line + long_text
            Opponent = None
            Opponent_window = random.randint(2,5)
            enemy_modifier += 0.5
        else:
            long_text = line + long_text
        if Player.period == 9 or Opponent_window == 1:
            long_text = f'<span style="color:red">ВНИМАНИЕ! В периоде {Player.period+1} появится конкурирующая компания!</span>' + '\n' + long_text
        if Player.period == 10 or (Opponent_window == 0 and Player.period > 2):
            long_text = '<span style="color:red">Появился конкурент на рынке</span>' + '\n' + long_text
        
        log = long_text
        Opponent_window -= 1
        if Player.period % 10 == 0 and Player.period > 10:
            demand_constant += 20

        # Генерируем случайную цену собственности для следующей покупки
        property_price = round(np.random.normal(100, 5),2)
        
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"status": "error on server", "message": str(e), "traceback": tb})
    return jsonify({ # Возвращаем данные, которые изменились после производства, обратно в Vue-приложение
        "status": "success",
        "received": production_amount,
        "money": Player.money,
        "costs": Player.cost[-1],
        "long_text": long_text,
        "health": Player.health,
        "demand": Player.demand,
        "property_price": property_price,
    })

# Перезагружает игру, сбрасывая все значения до начальных
@app.route('/reset', methods=['POST'])
def reset_game():
    global Player, log, Opponent, entry_cost, enemy_modifier, property_price, player_plots
    Player = Company(1000000, 0, [50])
    data = {
        'health': 100,
        'period': Player.period,
        'money': Player.money,
        'demand': 100,
        'costs': Player.cost[-1],
        'overallProduction': Player.overall_production,
        'long_text': 'Игра сброшена. Вы можете начать заново.',
        'property_price': 1000,
        'playersPlots': [],
    }
    property_price = 100
    enemy_modifier = 1
    player_plots.clear()
    entry_cost = 0
    Opponent = None
    log = data['long_text']
    return jsonify(data)

# Увеличивает стоимость производства на указанную величину для игрока и противника
@app.route('/increase_cost', methods=['POST'])
def increase_cost():
    global Player, base_cost
    data = request.get_json()
    amount = int(data.get('amount', 0)) # Получаем величину увеличения стоимости производства из запроса
    base_cost += amount
    Player.cost = [c + amount for c in Player.cost]
    return jsonify({'costs': Player.cost[-1]})

# Лоббирование игрока для входа на рынок
@app.route('/invest', methods=['POST'])
def invest():
    global Player, log, entry_cost
    data = request.get_json()
    invested_money = data.get('investedMoney') # Получаем сумму инвестиций из запроса
    action = data.get('action') # Получаем действие из запроса
    is_invested = data.get('isInvested')

    if invested_money <= Player.money:
        Player.money -= invested_money
        is_invested = True
        entry_cost += action
    
    # Возвращаем последствия лоббирования игрока в Vue-приложение
    response = { 
        "isInvested": is_invested,
        "newMoney": Player.money,
    }
    return jsonify(response)

# Покупка собственности игроком
@app.route('/buy_property', methods=['POST'])
def buy_property():
    global Player, log, property_price, Opponent, opponent_adcost, base_cost
    property_taxation = 0.005
    data = request.get_json()
    plots = data.get('plots')
    if Player.money >= property_price:
        Player.money -= property_price
        log = f'Вы приобрели собственность за {property_price} рублей.'
        player_plots.append(property_price)
        plots.append(property_price)
        Player.additional_cost += property_price * property_taxation # Увеличиваем стоимость существования компании игрока на величину налога на собственность
        Player.cost[-1] += round(property_price * property_taxation,2) # Увеличиваем стоимость производства игрока на величину налога на собственность

        if Opponent: # Если противник существует, увеличиваем его стоимость производства
            Opponent.additional_cost += property_price * property_taxation/2
            Opponent.cost[-1] += property_price * property_taxation
        else: # Если противник не существует, увеличиваем базовую стоимость производства
            opponent_adcost += property_price * property_taxation / 2
            base_cost += property_price * property_taxation / 2

        # Генерируем случайную цену собственности для следующей покупки
        property_price = round(np.random.normal(1000, 5), 2)
    response = {
        "status": "success",

        "playersPlots": plots,
        "money": Player.money,
        "property_price": property_price,
        "costs": Player.cost[-1],  # <-- Add this line
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_app(path):
    if path != "" and os.path.exists("dist/" + path):
        return send_from_directory('dist', path)
    else:
        return send_from_directory('dist', 'index.html')