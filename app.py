from flask import Flask, jsonify
from nselib import capital_market

app = Flask(__name__)

@app.route('/')
def index():
    try:
        data = capital_market.market_watch_all_indices()
        if data is None or not isinstance(data, list) or len(data) == 0:
            raise ValueError("Unexpected response format from API")
        return jsonify({"message": "API call successful", "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
