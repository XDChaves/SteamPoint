# app.py
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    games = pd.read_csv('DataCSV/games_limpo.csv', sep=',')
    dg_filter = games[["app_id","name","release_date","is_free","type"]]

    json_table_str = dg_filter.to_json(orient='table', indent=4, force_ascii=False)

    return json_table_str

if __name__ == '__main__':
    app.run(debug=True)