# app.py
from flask import Flask
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    dgames = pd.read_csv('.\\DataCSV\\games_limpo.csv', sep=',',on_bad_lines="skip")

    json_table_str = dgames.to_json(orient='table', indent=4, force_ascii=False)

    
    return json_table_str


if __name__ == '__main__':
    app.run(debug=True)