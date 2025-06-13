import random
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
    }
    return jsonify(data)

@app.route('/production', methods=['POST'])
def receive_production():
    global log, Opponent, Opponent_window, Player, demand_constant
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
                Opponent = Company(1000, 0, [50], period=1, demand=demand_constant, opponent=True, additional_cost=50)

            line, is_enemy_defeated = Player.produce(Opponent)
        if is_enemy_defeated:
            log = '<span style="color:green">Вы победили конкурента!</span>' + '\n' + long_text
            Opponent = None
            Opponent_window = random.randint(2,5)
        # print(Player.money)
        long_text = 'В период <span style="color:skyblue">{}</span> ваша компания произвела <span style="color:#ffc55b">{}</span> единиц продукции'.format(Player.period-1, Player.q) + '\n' + long_text
        long_text = 'В период <span style="color:skyblue">{}</span> прибыль от произведённой продукции составила <span style="color:#39f139">{}</span> рублей'.format(Player.period-1,round(Player.q * (Player.demand - Player.q) - Player.cost[-2] * Player.q,2)) + '\n' + long_text
        if Player.period == 9 or Opponent_window == 1:
            long_text = f'<span style="color:red">ВНИМАНИЕ! В периоде {Player.period+1} появится конкурирующая компания!</span>' + '\n' + long_text
        if Player.period == 10 or (Opponent_window == 0 and Player.period > 2):
            long_text = '<span style="color:red">Появился конкурент на рынке</span>' + '\n' + long_text
        
        long_text = line + long_text
        log = long_text
        Opponent_window -= 1
        if Player.period % 10 == 0 and Player.period > 10:
            demand_constant += 20
        # print(Player.health)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    return jsonify({
        "status": "success",
        "received": production_amount,
        "money": Player.money,
        "costs": Player.cost[-1],
        "long_text": long_text,
        "health": Player.health,
        "demand": Player.demand,
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    global Player, log, Opponent
    Player = Company(1000000, 0, [50])  # Reset to default values
    data = {
        'health': 100,
        'period': Player.period,
        'money': Player.money,
        'demand': 100,
        'costs': Player.cost[-1],
        'overallProduction': Player.overall_production,
        'long_text': 'Игра сброшена. Вы можете начать заново.',
    }
    Opponent = None
    log = data['long_text']
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)