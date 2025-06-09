from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Company

app = Flask(__name__)
CORS(app)

# Create a global player instance
Player = Company(1000000, 0, [50])
log = 'Игра запущена. Вы можете начать производить продукцию.'

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        'healthSpent': 0,
        'period': Player.period,
        'money': Player.money,  # Use Player's money
        'demand': '100 - Q',
        'costs': Player.cost[-1],  # Use Player's current cost
        'overallProduction': Player.overall_production,  # Use Player's overall production
        'long_text': log,
    }
    return jsonify(data)

@app.route('/production', methods=['POST'])
def receive_production():
    global log
    data = request.get_json()
    production_amount = data.get('productionAmount')
    long_text = data.get('longText')
    try:
        Player.q = int(production_amount)
        Player.produce()
        print(Player.money)
        long_text = 'компания произвела {} единиц продукции'.format(Player.q) + '\n' + long_text
        long_text = 'прибыль от произведённой продукции составила {} рублей'.format(Player.q * (100 - Player.q) - Player.cost[-1] * Player.q) + '\n' + long_text
        log = long_text
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    return jsonify({
        "status": "success",
        "received": production_amount,
        "money": Player.money,
        "costs": Player.cost[-1],
        "long_text": long_text,
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    global Player, log
    Player = Company(1000000, 0, [50])  # Reset to default values
    data = {
        'healthSpent': 0,
        'period': Player.period,
        'money': Player.money,
        'demand': '100 - Q',
        'costs': Player.cost[-1],
        'overallProduction': Player.overall_production,
        'long_text': 'Игра сброшена. Вы можете начать заново.',
    }
    log = data['long_text']
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)