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

# Função para executar a consulta SQL e retornar um DataFrame
def fetch_silver_data(engine):
    query = """
    SELECT
        nome_jogo,
        plataformas,
        data_lancamento,
        avaliacao,
        qtde_avaliacoes,
        nota_metacritic,
        tempo_de_jogo,
        ARRAY_LENGTH(regexp_split_to_array(plataformas, ','), 1) AS total_plataformas,
        EXTRACT(YEAR FROM data_lancamento) AS ano_lancamento
    FROM 
        silver_games
    WHERE 
        data_lancamento IS NOT NULL;
    """
    return pd.read_sql(query, engine)

# Função principal para orquestrar o processo
def main():
    # Carregar as variáveis de ambiente
    db_user, db_password, db_host, db_port, db_name = load_env_variables()
    
    # Criar a conexão com o banco de dados
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    # Obtém os dados da camada Silver
    df_gold = fetch_silver_data(engine)
    
    # Inserir dados na tabela gold_games
    df_gold.to_sql('gold_games', engine, if_exists='replace', index=False)

if __name__ == "__main__":
    main()
