from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Company

app = Flask(__name__)
CORS(app)

# Create a global player instance
Player = Company(1000000, 0, [50])
Opponent = None
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
    global log, Opponent
    data = request.get_json()
    production_amount = data.get('productionAmount')
    long_text = data.get('longText')
    try:
        Player.q = int(production_amount)
        if Player.period < 10:
            Player.produce()
        else:
            if Opponent is None:
                Opponent = Company(1000, 0, [50], period=11, demand=100, opponent=True, additional_cost=50)
            Player.produce(Opponent)
        # print(Player.money)
        long_text = 'В период <span style="color:skyblue">{}</span> ваша компания произвела <span style="color:#ffc55b">{}</span> единиц продукции'.format(Player.period-1, Player.q) + '\n' + long_text
        long_text = 'В период <span style="color:skyblue">{}</span> прибыль от произведённой продукции составила <span style="color:#39f139">{}</span> рублей'.format(Player.period-1,round(Player.q * (100 - Player.q) - Player.cost[-2] * Player.q,2)) + '\n' + long_text
        if Player.period == 9:
            long_text = '<span style="color:red">ВНИМАНИЕ! В периоде 10 появится конкурирующая компания!</span>' + '\n' + long_text
        if Player.period == 10:
            long_text = '<span style="color:red">Появился конкурент на рынке</span>' + '\n' + long_text
        log = long_text
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