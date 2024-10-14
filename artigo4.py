import requests
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine

# Função para carregar as variáveis de ambiente
def load_env_variables():
    load_dotenv()

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    api_key = os.getenv('API_KEY')

    if not all([db_user, db_password, db_host, db_port, db_name, api_key]):
        raise ValueError("Alguma variável de ambiente não está definida. Verifique o arquivo .env.")
   
    return db_user, db_password, db_host, db_port, db_name, api_key

# Função para fazer a requisição à API e coletar os dados dos jogos
def get_data(api_key, max_retries=5):
    url = "https://api.rawg.io/api/games"
    params = {
        "key": api_key,
        "page_size": 40
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Levanta um erro se o status não for 200
    games_data = response.json()
    return games_data

# Função para processar os dados e desaninhá-los
def process_games_data(games_data):
    # Cria uma lista para armazenar os dados desaninhados
    all_games = []

    for game in games_data['results']:
        # Coleta dados básicos
        game_info = {
            'name': game['name'],
            'released': game.get('released'),
            'rating': game.get('rating'),
            'rating_counts': game.get('ratings_count'),
            'metacritic': game.get('metacritic'),
            'playtime': game.get('playtime')
        }

        # Desaninha plataformas e requisitos
        platforms = []
        if 'platforms' in game:
            for platform in game['platforms']:
                platform_info = platform['platform']['name']  # Pega o nome da plataforma
                platforms.append(platform_info)  # Adiciona à lista de plataformas

        # Junta os dados do jogo com os dados das plataformas
        all_games.append({**game_info, 'platforms': ', '.join(platforms)})  # Concatena as plataformas em uma string

    return all_games

# Função principal
def main():
    # Carregar variáveis de ambiente
    db_user, db_password, db_host, db_port, db_name, api_key = load_env_variables()

    # Criar a engine de conexão 
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    # Coletar dados dos jogos
    games_data = get_data(api_key)

    # Processar os dados para desaninhá-los
    processed_data = process_games_data(games_data)

    # Inserir os dados no banco de dados
    if processed_data:
        df = pd.DataFrame(processed_data)  # Cria um DataFrame a partir dos dados processados
        df.to_sql('bronze_games', engine, if_exists='replace', index=False)  # Armazena o DataFrame na tabela
        print("Dados inseridos com sucesso na tabela bronze_games.")
    else:
        print("Nenhum dado foi coletado da API.")

# Executar a função principal
if __name__ == "__main__":
    main()
