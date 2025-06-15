import random
import traceback
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Company

app = Flask(__name__)
CORS(app)

# Create a global player instance
Player = Company(1000000, 0, [50])  # Initial values
Opponent = None
Opponent_window = 0
demand_constant = 100
base_cost = 50
entry_cost = 0
enemy_modifier = 1
property_price = 1000
player_plots = []
opponent_adcost = 0

log = 'Игра запущена. Выберите количество продукции для производства.'

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        'health': Player.health,
        'period': Player.period,
        'money': Player.money,  # Use Player's money
        'demand': 100,
        'costs': Player.cost[-1],  # Use Player's current cost
        'overallProduction': Player.overall_production,  # Use Player's overall production
        'long_text': log,
        'property_price': property_price,
        'playersPlots': player_plots,
    }
    return jsonify(data)

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
            line, is_enemy_defeated = Player.produce()
        else:
            if Player.period == 10 or (Opponent_window == -1 and Player.period > 2):
                Opponent = Company(1000*enemy_modifier, 0, [base_cost], period=1, demand=demand_constant, opponent=True, additional_cost=opponent_adcost, one_time_cost=entry_cost)

            line, is_enemy_defeated = Player.produce(Opponent)
        # print(Player.money)
        long_text = 'В период <span style="color:skyblue">{}</span> ваша компания произвела <span style="color:#ffc55b">{}</span> единиц продукции'.format(Player.period-1, Player.q) + '\n' + long_text
        long_text = 'В период <span style="color:skyblue">{}</span> прибыль от произведённой продукции составила <span style="color:#39f139">{}</span> рублей'.format(Player.period-1,round(Player.q * (Player.demand - Player.q) - Player.cost[-2] * Player.q - Player.additional_cost,2)) + '\n' + long_text
        if is_enemy_defeated:
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

        property_price = round(np.random.normal(100, 5),2)
        # print(Player.health)
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"status": "error on server", "message": str(e), "traceback": tb})
    return jsonify({
        "status": "success",
        "received": production_amount,
        "money": Player.money,
        "costs": Player.cost[-1],
        "long_text": long_text,
        "health": Player.health,
        "demand": Player.demand,
        "property_price": property_price,
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    global Player, log, Opponent, entry_cost, enemy_modifier, property_price, player_plots
    Player = Company(1000000, 0, [50])  # Reset to default values
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

@app.route('/increase_cost', methods=['POST'])
def increase_cost():
    global Player, base_cost
    data = request.get_json()
    amount = int(data.get('amount', 0))
    base_cost += amount
    Player.cost = [c + amount for c in Player.cost]
    return jsonify({'costs': Player.cost[-1]})

@app.route('/invest', methods=['POST'])
def invest():
    global Player, log, entry_cost
    data = request.get_json()
    invested_money = data.get('investedMoney')
    action = data.get('action')
    is_invested = data.get('isInvested')

    if invested_money <= Player.money:
        Player.money -= invested_money
        is_invested = True
        entry_cost += action
    # Example logic: just echo back some dummy values
    response = {
        "isInvested": is_invested,
        "newMoney": Player.money,
    }
    return jsonify(response)

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
        Player.additional_cost += property_price * property_taxation
        Player.cost[-1] += round(property_price * property_taxation,2)

        if Opponent:
            Opponent.additional_cost += property_price * property_taxation/2
            Opponent.cost[-1] += property_price * property_taxation
        else:
            opponent_adcost += property_price * property_taxation / 2
            base_cost += property_price * property_taxation / 2

        property_price = round(np.random.normal(1000, 5), 2)
    response = {
        "status": "success",
        "playersPlots": plots,
        "money": Player.money,
        "property_price": property_price,
        "costs": Player.cost[-1],  # <-- Add this line
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)