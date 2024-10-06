# Data Warehousing 101 - Códigos dos Artigos do Blog

Este repositório contém os códigos utilizados no projeto **Data Warehousing 101**, uma série de artigos que explicam desde a coleta de dados até a criação de dashboards em um pipeline completo de Data Warehousing.

Os artigos estão disponíveis no site [blog.insideboo.com](https://blog.insideboo.com).

## Estrutura dos Artigos

### 1 - Introdução e cultura de dados

Uma visão geral da importância de cultura de dados dentro das organizações e como projetos de Data Warehousing podem ajudar na tomada de decisões.

### 2 - Coletando dados de uma API REST com Bearer Token em Python

1. Como selecionar uma API e obter o token de autenticação.
2. Instalação de bibliotecas e configuração do ambiente.
3. Criação do código Python para realizar a requisição e extrair dados.
4. Verificação da consistência e formato dos dados.
5. Como lidar com limites de requisição e erros de integração.

### 3 - Tratando os Dados da API

1. Verificando consistência e formato dos dados.
2. Lidando com limites de requisição e exceções.

### 4 - Criando o banco de dados e estrutura do data warehouse

1. Instalando e configurando o PostgreSQL com Docker.
2. Criação de schemas e tabelas para as camadas Bronze, Silver e Gold.
3. Dicas de modelagem de dados.
4. Inserindo dados na camada Bronze.
5. Criação de índices e otimizações.

### 5 - Implementando transformações nas camadas silver e gold

1. Limpeza e normalização dos dados com Pandas.
2. Armazenamento dos dados transformados (append com histórico).
3. Criação de tabelas prontas para análise na camada Gold.
4. Automatizando as transformações com scripts Python.

### 6 - Configurando o Airflow para orquestrar o pipeline de dados

1. Instalação do Airflow com Docker.
2. Criação da primeira DAG para ETL.
3. Configuração de agendamentos e dependências.
4. Monitorando o pipeline através da interface do Airflow.

### 7 - Implementando tolerância a falhas e segurança no pipeline

1. Retries e alertas no Airflow.
2. Estratégias de recuperação de falhas.
3. Monitoramento e logging no Airflow.
4. Boas práticas de segurança, incluindo o uso de tokens com Vault.

### 8 - Containerizando todo o projeto com Docker Compose

1. Explicação sobre Docker Compose e suas vantagens
2. Criação do arquivo `docker-compose.yml` para PostgreSQL, Airflow, e scripts Python.
3. Deploy e teste do ambiente completo.
4. Manutenção do ambiente Dockerizado.

### 9 - Construindo um dashboard no Power BI com dados do data warehouse

1. Conectando o Power BI ao PostgreSQL.
2. Importação de dados das camadas Gold.
3. Criação de visualizações e dashboards interativos.
4. Publicação e compartilhamento de relatórios.

### 10 - Revisão do projeto completo e próximos passos

1. Revisão de todos os componentes construídos.
2. Considerações sobre escalabilidade e monitoramento com Grafana.
3. Próximos passos para expandir o projeto (ex: machine learning, mais fontes de dados).