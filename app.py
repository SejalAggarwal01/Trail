from flask import Flask, jsonify
from nsepython import nse_eq
from nselib import capital_market
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_indices():
    try:
        data = capital_market.market_watch_all_indices()
        last = data['last']
        index_symbol = data['indexSymbol']
        result = []
        for sym, lst in zip(index_symbol, last):
            result.append({
                'last': int(lst),
                'indexSymbol': sym
            })
        return result
    except Exception as e:
        return {'error': str(e)}


@app.route('/api/get_stock_info', methods=['GET'])
def indices():
    response_data = get_indices()
    return jsonify(response_data)

