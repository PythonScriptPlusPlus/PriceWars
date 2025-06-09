from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Company

app = Flask(__name__)
CORS(app)

# Create a global player instance
Player = Company(1000000, 0, [50])

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        'healthSpent': 0,
        'period': Player.period,
        'money': Player.money,  # Use Player's money
        'demand': '100 - Q',
        'costs': Player.cost[-1],  # Use Player's current cost
        'overallProduction': Player.overall_production,  # Use Player's overall production
    }
    return jsonify(data)

@app.route('/production', methods=['POST'])
def receive_production():
    data = request.get_json()
    production_amount = data.get('productionAmount')
    try:
        Player.q = int(production_amount)
        Player.produce()
        print(Player.money)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    return jsonify({
        "status": "success",
        "received": production_amount,
        "money": Player.money,
        "costs": Player.cost[-1]
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    global Player
    Player = Company(1000000, 0, [50])  # Reset to default values
    data = {
        'healthSpent': 0,
        'period': Player.period,
        'money': Player.money,
        'demand': '100 - Q',
        'costs': Player.cost[-1],
        'overallProduction': Player.overall_production,
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)