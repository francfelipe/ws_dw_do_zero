# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# import das minhas variaveis de ambiente

# definir os ativos que eu quero buscar
commodities   = ['CL=F', 'GC=F', 'SI=F']

# carregar as variaveis de ambiente
load_dotenv()
DB_HOST       = os.getenv('DB_HOST_PROD')
DB_PORT       = os.getenv('DB_PORT_PROD')
DB_NAME       = os.getenv('DB_NAME_PROD')
DB_USER       = os.getenv('DB_USER_PROD')
DB_PASS       = os.getenv('DB_PASS_PROD')
DB_SCHEMA     = os.getenv('DB_SCHEMA_PROD')

# criar a string de conexão com o banco de dados
DATABASE_PROD = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# criar a conexão com o banco de dados
engine = create_engine(DATABASE_PROD)

def buscar_dados_commodities(simbolo, periodo='10y', intervalo='1d'):
    '''
    Função para buscar os dados de commodities
    Args:
        simbolo (str): simbolo do ativo
        periodo (str): periodo de busca
        intervalo (str): intervalo de busca
    '''
    # realiza a consula
    ticker = yf.Ticker(simbolo)
    # busca os dados
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    # insere a coluna simbolo
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_dados_commodities(commodities):
    '''
    Função para buscar os dados de commodities
    '''
    # criar um dataframe vazio
    todos_dados=[]
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

def salvar_no_postgres(df, schema=DB_SCHEMA):
    df.to_sql('commodities', con=engine, schema=schema, if_exists='replace', index=True, index_label='Date')

if __name__ == '__main__':
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados, schema=DB_SCHEMA)
    
    
# concatenar os meus ativos (1... 2... 3) -> (1)

# Salvar no meu banco de dados