from flask import Flask, jsonify
from nsepython import nse_eq
from nselib import capital_market
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)


if 'RENDER' in os.environ:  # Check if running on Render
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
else:
    # Set up logging to a file for local development
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(filename=os.path.join(log_dir, 'error.log'), level=logging.DEBUG)


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
        app.logger.error("Error occurred in get_indices: %s", str(e), exc_info=True)
        return {f'error',str(e)}



@app.route('/api/get_stock_info', methods=['GET'])
def indices():
    response_data = get_indices()
    return jsonify(response_data)
