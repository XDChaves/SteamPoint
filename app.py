from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import time
from steam_scraper import get_top_games_steam_stats

app = Flask(__name__)
CORS(app)

# Variáveis para o cache
cached_top_games = None
last_fetch_time = 0
# Duração do cache: 30 minutos a 1 hora (em segundos)
CACHE_DURATION_SECONDS = 30 * 60 # 30 minutos
# CACHE_DURATION_SECONDS = 60 * 60 # 1 hora

tags_csv = 'DataCSV/tags.csv'

games_csv = 'DataCSV/games.csv'

steamspy_csv = 'DataCSV/steamspy_insights.csv'

reviews_csv = 'DataCSV/review.csv'

categories_csv = 'DataCSV/categories.csv'
["app_id","category"]

promotional_csv = 'DataCSV/promotional.csv'

# Rota para obter os top 10 jogos da Steam
@app.route('/api/top-games', methods=['GET'])
def top_games():
    global cached_top_games, last_fetch_time # Declara para poder modificar as variáveis globais

    current_time = time.time()

    # Verifica se o cache está vazio ou se expirou
    if cached_top_games is None or (current_time - last_fetch_time > CACHE_DURATION_SECONDS):
        print("Cache expirado ou vazio. Buscando novos dados da Steam...")
        try:
            fresh_data = get_top_games_steam_stats() # Chama a função de scraping
            if fresh_data: # Se os dados foram obtidos com sucesso
                cached_top_games = fresh_data
                last_fetch_time = current_time
                print("Dados atualizados e armazenados em cache.")
            else:
                # Se o scraping não retornou dados mas não levantou exceção
                print("Scraping não retornou dados, mantendo o cache antigo se existir.")
                if cached_top_games is None: # Se não há dados antigos, retorna erro
                    return jsonify({"error": "Não foi possível obter dados dos jogos no momento."}), 500
        except Exception as e:
            print(f"Erro inesperado ao buscar dados via scraping: {e}")
            if cached_top_games is None: # Se não há dados antigos e houve erro
                return jsonify({"error": "Não foi possível obter dados dos jogos no momento."}), 500
    else:
        print("Retornando dados do cache (válido).")

    return jsonify(cached_top_games)

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

@app.route('/review')
def steam_reviews():
    games= pd.read_csv(games_csv, sep=',')
    dg_filter = games[["app_id", "name"]]

    drev = pd.read_csv('DataCSV/review.csv', sep=',', low_memory=False)
    filtered = drev[["app_id","review_score","review_score_description","positive","negative","total","metacritic_score","recommendations"]]

    df = pd.merge(dg_filter, filtered, on='app_id', how='inner')

    json_data_rev = df.to_json(orient='table', indent=9, force_ascii=False)

    return json_data_rev

@app.route('/tags')
def steam_tags():
    games= pd.read_csv(games_csv, sep=',')
    dg_filter = games[["app_id", "name"]]

    dtag = pd.read_csv('DataCSV/tags.csv', sep=',')
    filtered = dtag[["app_id","tag"]]

    df = pd.merge(dg_filter, filtered, on='app_id', how='inner')

    json_data_tag = df.to_json(orient='table', indent=3, force_ascii=False)

    return json_data_tag

#Fazendo merge com Reviews
@app.route('/rev-all')
def rev_all():
    rev = pd.read_csv('DataCSV/all_data_combined_filtered.csv', sep=',', low_memory=False)

    json_data_all = rev.to_json(orient='table', indent=3, force_ascii=False)

    return json_data_all

if __name__ == '__main__':
    app.run(debug=True)