import requests
from dotenv import load_dotenv
import os
import time

# Carregar as variáveis de ambiente
load_dotenv()

# Recuperar o token de API do arquivo .env
api_key = os.getenv("API_KEY")

# Definir a URL da API com parâmetros diretamente na URL
url = "https://api.rawg.io/api/games"
params = {
    "key": api_key,
    "page_size": 20  # Número de jogos por página (ajuste conforme necessário)
}

max_retries = 5
retry_count = 0

while retry_count < max_retries:
    # Fazer a requisição GET para a API
    response = requests.get(url, params=params)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Extrair os dados em formato JSON
        data = response.json()

        # Verificar se os dados esperados estão presentes
        if "results" in data:
            # Iterar sobre os jogos retornados
            for game in data["results"]:
                print(f"Nome do jogo: {game['name']}")
                print(f"Data de lançamento: {game.get('released', 'Data não disponível')}")
                print(f"Rating: {game.get('rating', 'Rating não disponível')}")
                print("-" * 40)
            break
        else:
            print("Dados incompletos: Faltando 'results'.")
            break

    elif response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        print(f"Limite de requisições atingido. Tentando novamente em {retry_after} segundos.")
        time.sleep(retry_after)
        retry_count += 1

    else:
        print(f"Falha ao acessar a API: {response.status_code}")
        break
