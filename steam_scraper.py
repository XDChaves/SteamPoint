# steam_scraper.py
import requests
from bs4 import BeautifulSoup
import json

def get_top_games_steam_stats():
    url = "https://store.steampowered.com/stats/stats/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status() # Lança um erro para status de erro HTTP

    soup = BeautifulSoup(response.text, 'html.parser')

    top_games = []
        
    detail_stats_div = soup.find('div', id='detailStats')

    if detail_stats_div:
            game_rows = detail_stats_div.find_all('tr', class_='player_count_row')
            
            for i, row in enumerate(game_rows):
                if i >= 10: 
                    break # Pega apenas os top 10

                cols = row.find_all('td')

                if len(cols) >= 4: # Garante que há colunas suficientes
                    # 1. Jogadores agora (Current Players)
                    current_players_span = cols[0].find('span', class_='currentServers')
                    current_players_str = current_players_span.get_text(strip=True) if current_players_span else "0"
                    # Remover vírgulas e converter para int
                    current_players = int(current_players_str.replace(',', ''))

                    # 2. Pico diário (Daily Peak)
                    daily_peak_span = cols[1].find('span', class_='currentServers')
                    daily_peak_str = daily_peak_span.get_text(strip=True) if daily_peak_span else "0"
                    daily_peak = int(daily_peak_str.replace(',', ''))

                    # 3. Nome do Jogo
                    game_link_tag = cols[3].find('a', class_='gameLink')
                    game_name = game_link_tag.get_text(strip=True) if game_link_tag else "Nome Desconhecido"
                    
                    # 4. URL do Jogo
                    game_url = game_link_tag['href'] if game_link_tag and 'href' in game_link_tag.attrs else "#"

                    top_games.append({
                        "rank": i + 1,
                        "name": game_name,
                        "current_players": current_players,
                        "daily_peak_players": daily_peak,
                        "game_url": game_url
                    })
    return top_games