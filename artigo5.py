import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Função para carregar as variáveis de ambiente
def load_env_variables():
    load_dotenv()

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise ValueError("Alguma variável de ambiente não está definida. Verifique o arquivo .env.")
   
    return db_user, db_password, db_host, db_port, db_name

# Função para renomear colunas e transformar a data
def transform_bronze_to_silver(engine):
    # Extrair os dados da tabela bronze_games
    query = "SELECT * FROM bronze_games"
    df = pd.read_sql(query, engine)

    # Renomear as colunas
    df = df.rename(columns={
        'name': 'nome_jogo',
        'released': 'data_lancamento',
        'rating': 'avaliacao',
        'rating_counts': 'qtde_avaliacoes',
        'metacritic': 'nota_metacritic',
        'playtime': 'tempo_de_jogo',
        'platforms': 'plataformas'
    })

    # Transformar o campo 'data_lancamento' para o formato timestamp
    df['data_lancamento'] = pd.to_datetime(df['data_lancamento'], errors='coerce')

    return df

# Função principal
def main():
    # Carregar variáveis de ambiente e criar a engine de conexão
    db_user, db_password, db_host, db_port, db_name = load_env_variables()  # Função para carregar variáveis de ambiente
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    # Transformar os dados da tabela bronze
    transformed_data = transform_bronze_to_silver(engine)

    # Salvar os dados transformados na camada silver (pode ser uma nova tabela ou sobrescrever)
    transformed_data.to_sql('silver_games', engine, if_exists='replace', index=False)
    print("Dados transformados e inseridos na tabela silver_games.")

# Executar a função principal
if __name__ == "__main__":
    main()