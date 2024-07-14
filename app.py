from flask import Flask, jsonify
from nselib import Nse

app = Flask(__name__)
nse = Nse()

@app.route('/api/get_stock_info', methods=['GET'])
def get_stock_info():
    stock_data = nse.get_quote('TCS')
    return jsonify(stock_data)