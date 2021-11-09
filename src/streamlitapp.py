import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessamento.preprocessamento import Preproc


def FilterJogadores(df, id, times, agentes, mapas):

    if len(times) > 0: df = df[df['Time'].isin(times)]
    if len(agentes) > 0: df = df[df['Agente'].isin(agentes)]
    if len(mapas) > 0: df = df[df['Mapa'].isin(mapas)]
    df_antes = df[df['ID Partida'] <= id]
    df_depois = df[df['ID Partida'] >= id]

    return df_antes, df_depois

def FilterTimes(df, id, times, mapas):

    if len(times) > 0: df = df[df['Time'].isin(times)]
    if len(mapas) > 0: df = df[df['Mapa'].isin(mapas)]
    df_antes = df[df['ID Partida'] <= id]
    df_depois = df[df['ID Partida'] >= id]

    return df_antes, df_depois

def Distplot(df, col):

    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 9,
          'axes.labelsize': 12,
          'xtick.labelsize': 9,
          'ytick.labelsize': 14}
    
    plt.rcParams.update(rc)
    bins =  1 + 3.322*np.log(df[col].nunique())
    fig, ax = plt.subplots()
    
    ax = sns.histplot(data=df, x=col, bins=int(bins), color='#dc3d4b')
    plt.axvline(df[col].mean(), 0,1, color='white')
    
    ax.set_title(f'Distribuição de {col}', fontsize = 16)
    ax.set_xlabel(col, fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel('Quantidade', fontsize = 12)
    
    st.pyplot(fig)

def Countplot(df, col,num_obj):

    ## filtrando por top N mais frequentes
    dados_plot = df[df[col].isin( list(df[col].value_counts()[:num_obj].index) )]
    
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 9,
          'axes.labelsize': 12,
          'xtick.labelsize': 9,
          'ytick.labelsize': 14}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ax = sns.countplot(y = col, 
                        data = dados_plot, order=dados_plot[col].value_counts().index, 
                        palette=['#f94555', '#f2636b', '#672e37', '#7e7c7d', '#ce9e9c'])
    ax.set_title(str(col), fontsize = 16)
    ax.set_xlabel('Quantidade', fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel(col, fontsize = 12)
  
    st.pyplot(fig)

df_jogadores, df_times = Preproc()

TIMES = df_times.Time.unique()
AGENTES = df_jogadores.Agente.unique()
MAPAS = df_times.Mapa.unique()
ID_PARTIDA = df_times['ID Partida'].unique()

st.title("APP VISUALIZAÇÃO DADOS VALORANT")
st.image('../img/VALORANT_LOGO.png', width = 750)

##QUAIS FILTROS EU QUERO PARA OS DADOS
# TIMES
# AGENTES
# MAPAS
# "DATA" - POR MATCH_ID. EXPLICAR AS DATAS
# 

filtro_times = st.sidebar.multiselect('Filtro de Times', TIMES)
filtro_agentes = st.sidebar.multiselect('Filtro de Agentes', AGENTES)
filtro_mapas = st.sidebar.multiselect('Filtro de Mapas', MAPAS)
filtro_id = st.sidebar.select_slider('Filtro de Partidas - ID abaixo de 7000 correspondem a partidas de 2020', 
                    options=df_times['ID Partida'].unique())


## Amostra das bases
row1_spacer1, row1_1, row1_spacer2, row1_2, row1_spacer3  = st.columns((.2, 4, .4, 4, .2))
with row1_1:
    ''' ## Dados de Jogadores - Amostra de 20 Jogadores'''
    st.write(df_jogadores.sample(20,replace=True))
with row1_2:
    ''' ## Dados de Times - Amostra de 20 Times'''
    st.write(df_times.sample(20, replace=True))
st.markdown('''---''')

## Dados Times Filtrados
row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3  = st.columns((.2, 4, .4, 4, .2))
filter_times_antigo, filter_times_novo = FilterTimes(df_times, filtro_id, filtro_times, filtro_mapas)
with row2_1:
    f'''### Dados Filtrados Times - Antes ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_times_antigo.shape[0]}')
    st.write(filter_times_antigo)
with row2_2:
    f'''### Dados Filtrados Times - Depois ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_times_novo.shape[0]}')
    st.write(filter_times_novo)

## Sidebar -----------------------
st.sidebar.markdown(''' 
---
## Filtros dos gráficos de Times
''')
col_count_time = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Contagem Times', options = df_times.select_dtypes(include=['object']).columns, index=1)
col_dist_jogador = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Distribuição', options = df_times.select_dtypes(exclude=['object']).columns, index=1)
num_obj = st.sidebar.slider('Quantidade de valores do gráfico de Contagem', min_value=1, max_value=20, value=20)
## -------------------------------

## Graficos de Contagem Times -- Antes x Depois
row3_spacer1,row3_1, row3_spacer2, row3_2, row3_spacer3  = st.columns((.2, 2, .4, 2, .2))
with row3_1:
    f'''### Gráfico de Contagem - Dados Antes ID {filtro_id}'''
    Countplot(filter_times_antigo, col_count_time, num_obj)
with row3_2:
    f'''### Gráfico de Contagem - Dados Após ID {filtro_id}'''
    Countplot(filter_times_novo, col_count_time, num_obj)

## Graficos de Distribuicao Times -- Antes x Depois
row4_spacer1,row4_1, row4_spacer2, row4_2, row4_spacer3  = st.columns((.2, 2, .4, 2, .2))
with row4_1:
    f'''### Gráfico de Distribuição - Dados Antes ID {filtro_id}'''
    Distplot(filter_times_antigo, col_dist_jogador)
with row4_2:
    f'''### Gráfico de Distribuição - Dados Após ID {filtro_id}'''
    Distplot(filter_times_novo, col_dist_jogador    )

## Sidebar -----------------------
st.sidebar.markdown(''' 
---
## Filtros dos gráficos de Jogadores
''')

col_count_jogador = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Contagem - Jogadores', options = df_jogadores.select_dtypes(include=['object']).columns)
col_dist_jogador = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Distribuição - Jogadores', options = df_jogadores.select_dtypes(exclude=['object']).columns)
#num_obj = st.sidebar.slider('Quantidade de observações do gráfico', min_value=1, max_value=20)
## -------------------------------
st.markdown('''---''')
## Dados Jogadores Filtrados
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 4, .4, 4, .2))
filter_jogador_antigo, filter_jogador_novo = FilterJogadores(df_jogadores, filtro_id, filtro_times, filtro_agentes, filtro_mapas)
with row5_1:
    '''### Dados Filtrados Jogadores - Antes ID'''
    st.write(f'Total de Linhas - {filter_jogador_antigo.shape[0]}')
    st.write(filter_jogador_antigo)
with row5_2:
    '''### Dados Filtrados Jogadores - Depois ID'''
    st.write(f'Total de Linhas - {filter_jogador_novo.shape[0]}')
    st.write(filter_jogador_novo)

## Graficos de Contagem Times -- Antes x Depois
row3_spacer1,row3_1, row3_spacer2, row3_2, row3_spacer3  = st.columns((.2, 2, .4, 2, .2))
with row3_1:
    f'''### Gráfico de Distribuição - Dados Antes ID {filtro_id}'''
    Distplot(filter_jogador_antigo, col_dist_jogador)
    Countplot(filter_jogador_antigo, col_count_jogador, num_obj)
with row3_2:
    f'''### Gráfico de Distribuição - Dados Após ID {filtro_id}'''
    Distplot(filter_jogador_novo, col_dist_jogador)
    Countplot(filter_jogador_novo, col_count_jogador, num_obj)