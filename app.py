# app.py
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)
CORS(app)

@app.route('/steam-games')
def games():
    games = pd.read_csv('DataCSV/games_limpo.csv', sep=',')
    dg_filter = games[["app_id","name","release_date","is_free","type"]]
    json_table_str = dg_filter.to_json(orient='table', indent=4, force_ascii=False)

    return json_table_str

@app.route('/steam-games-insights')
def games_insights():
    games = pd.read_csv('DataCSV/games_limpo.csv', sep=',')
    dg_filter = games[["app_id","name"]]

    dspy = pd.read_csv('.\\DataCSV\\steamspy_insights.csv', sep=',')
    ds_filter = dspy[["app_id","developer","publisher","languages","genres"]]

    df = pd.merge(dg_filter, ds_filter, on='app_id', how='inner')

    json_data_insights = df.to_json(orient='table', indent=4, force_ascii=False)

    return json_data_insights

if __name__ == '__main__':
    app.run(debug=True)