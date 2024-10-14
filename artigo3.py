import requests
from dotenv import load_dotenv
import os
import time
import csv

# Carregar as variáveis de ambiente
load_dotenv()

# Recuperar o token de API do arquivo .env
api_key = os.getenv("API_KEY")

# Definir a URL da API com parâmetros diretamente na URL
url = "https://api.rawg.io/api/games"
params = {
    "key": api_key,
    "page_size": 15  # Número de jogos por página
}

max_retries = 5
retry_count = 0

# Criar e abrir o arquivo CSV para escrita
with open('games_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    # Nomes das colunas em inglês e camelCase
    fieldnames = ['gameName', 'releaseDate', 'rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Escrever o cabeçalho no arquivo CSV
    writer.writeheader()

    while retry_count < max_retries:
        try:
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
                        # Escrever os dados do jogo no arquivo CSV
                        writer.writerow({
                            'gameName': game['name'],
                            'releaseDate': game.get('released', 'Data não disponível'),
                            'rating': game.get('rating', 'Rating não disponível')
                        })
                    break  # Saia do loop após sucesso

                else:
                    print("Dados incompletos: Faltando 'results'.")
                    break

            elif response.status_code == 429:
                # Limite de requisições atingido
                retry_after = int(response.headers.get("Retry-After", 60))
                print(f"Limite de requisições atingido. Tentando novamente em {retry_after} segundos.")
                time.sleep(retry_after)
                retry_count += 1

            else:
                print(f"Falha ao acessar a API: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao acessar a API: {e}")
            retry_count += 1
            time.sleep(5)  # Aguardar 5 segundos antes de tentar novamente

        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")
            break