# import
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# import das minhas variaveis de ambiente

commodities = ['CL=F', 'GC=F', 'SI=F']

def buscar_dados_commodities(simbolo, periodo='5y', intervalo='1d'):
    '''
    Função para buscar os dados de commodities
    Args:
        simbolo (str): simbolo do ativo
        periodo (str): periodo de busca
        intervalo (str): intervalo de busca
    '''
    # realiza a consula
    ticker = yf.Ticker('CL=F')
    # busca os dados
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    # insere a coluna simbolo
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_dados_commoties(commodities):
    '''
    Função para buscar os dados de commodities
    '''
    # criar um dataframe vazio
    todos_dados=[]
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

if __name__ == '__main__':
    dados_concatenados = buscar_todos_dados_commoties(commodities)
    print(dados_concatenados)
    
    
# concatenar os meus ativos (1... 2... 3) -> (1)

# Salvar no meu banco de dados