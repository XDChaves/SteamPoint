from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)


games_csv = 'DataCSV/games.csv'
steamspy_csv = 'DataCSV/steamspy_insights.csv'
reviews_csv = 'DataCSV/review.csv'
promotional_csv = 'DataCSV/promotional.csv'
categories_csv = 'DataCSV/categories.csv'
tags_csv = 'DataCSV/tags.csv'


@app.route('/steam-games')
def steam_games():
    games_df = pd.read_csv(games_csv, sep=',')
    dg_filter = games_df[["app_id", "name", "release_date", "is_free", "type"]]

    json_table_str = dg_filter.to_json(orient='table', indent=4, force_ascii=False)
    
    return json_table_str

@app.route('/game/<int:app_id>')
def get_game_details(app_id):
    try:
        game_details = {}

        # Ler e filtrar games.csv
        games_df = pd.read_csv(games_csv, sep=',')
        game_data = games_df[games_df['app_id'] == app_id][["app_id", "name", "release_date", "is_free", "type"]].to_dict(orient='records')
        game_details['game'] = game_data[0] if game_data else None

        # Ler e filtrar steamspy_insights.csv
        steamspy_df = pd.read_csv(steamspy_csv, sep=',')
        steamspy_data = steamspy_df[steamspy_df['app_id'] == app_id][["app_id", "developer", "publisher", "languages", "genres"]].to_dict(orient='records')
        game_details['steamspy'] = steamspy_data[0] if steamspy_data else None

        # Ler e filtrar review.csv
        reviews_df = pd.read_csv(reviews_csv, sep=',', low_memory=False)
        review_data = reviews_df[reviews_df['app_id'] == app_id][["app_id", "review_score", "review_score_description", "positive", "negative", "total", "metacritic_score", "recommendations"]].to_dict(orient='records')
        game_details['review'] = review_data[0] if review_data else None

        # Ler e filtrar promotional.csv
        promotional_df = pd.read_csv(promotional_csv, sep=',')
        promotional_data = promotional_df[promotional_df['app_id'] == app_id][["app_id", "header_image", "background_image"]].to_dict(orient='records')
        game_details['promotional'] = promotional_data[0] if promotional_data else None

        # Ler e filtrar categories.csv
        categories_df = pd.read_csv(categories_csv, sep=',')
        category_data = categories_df[categories_df['app_id'] == app_id][["app_id", "category"]].to_dict(orient='records')
        game_details['categories'] = [item['category'] for item in category_data] if category_data else []

        # Ler e filtrar tags.csv
        tags_df = pd.read_csv(tags_csv, sep=',')
        tag_data = tags_df[tags_df['app_id'] == app_id][["app_id", "tag"]].to_dict(orient='records')
        game_details['tags'] = [item['tag'] for item in tag_data] if tag_data else []

        if game_details['game']:
            return jsonify(game_details)
        else:
            return jsonify({'error': 'Game not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/steam-games-insights')
def games_insights():
    games= pd.read_csv(games_csv, sep=',')
    dg_filter = games[["app_id", "name"]]

    dspy = pd.read_csv('DataCSV/steamspy_insights.csv', sep=',')
    filter = dspy[["app_id","developer","publisher","languages","genres"]]

    df = pd.merge(dg_filter, filter, on='app_id', how='inner')

    json_data_insights = df.to_json(orient='table', indent=4, force_ascii=False)

    return json_data_insights

@app.route('/categories')
def steam_categories():
    games= pd.read_csv(games_csv, sep=',')
    dg_filter = games[["app_id", "name"]]

    dcat = pd.read_csv('DataCSV/categories.csv', sep=',')
    filtered = dcat[["app_id","category"]]

    df = pd.merge(dg_filter, filtered, on='app_id', how='inner')

    json_data_cat = df.to_json(orient='table', indent=3, force_ascii=False)

    return json_data_cat

@app.route('/tags')
def steam_tags():
    games= pd.read_csv(games_csv, sep=',')
    dg_filter = games[["app_id", "name"]]

    dtag = pd.read_csv('DataCSV/tags.csv', sep=',')
    filtered = dtag[["app_id","tag"]]

    df = pd.merge(dg_filter, filtered, on='app_id', how='inner')

    json_data_tag = df.to_json(orient='table', indent=3, force_ascii=False)

    return json_data_tag


if __name__ == '__main__':
    app.run(debug=True)