import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessamento.preprocessamento import Preproc

st.set_option('deprecation.showPyplotGlobalUse', False)


def FilterJogadores(df, id, times, agentes, mapas):

    if len(times) > 0: df = df[df['Time'].isin(times)]
    if len(agentes) > 0: df = df[df['Agente'].isin(agentes)]
    if len(mapas) > 0: df = df[df['Mapa'].isin(mapas)]
    df_antes = df[df['ID Partida'] <= id]
    df_depois = df[df['ID Partida'] >= id]

    return df_antes, df_depois

def FilterTimes(df, id, times, agentes, mapas):

    if len(times) > 0: df = df[df['Time'].isin(times)]
    #if len(agentes) > 0: df = df[df['Time'].isin(agentes)]
    if len(mapas) > 0: df = df[df['Mapa'].isin(mapas)]
    df_antes = df[df['ID Partida'] <= id]
    df_depois = df[df['ID Partida'] >= id]

    return df_antes, df_depois

def Distplot(df, col):

    bins =  1 + 3.322*np.log(df[col].nunique())
    fig, ax = plt.subplots(figsize=(7,3))
    
    ax = sns.histplot(data=df, x=col, bins=int(bins))
    plt.axvline(df[col].mean(), 0,1, color='red')
    
    ax.set_title(f'Distribuição de {col}', fontsize = 16)
    ax.set_xlabel(col, fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel('Quantidade', fontsize = 12)
    
    return fig

def Countplot(df, col,num_obj):

    ## filtrando por top N mais frequentes
    dados_plot = df[df[col].isin( list(df[col].value_counts()[:num_obj].index) )]

    fig, ax = plt.subplots(figsize=(7,3))
    ax = sns.countplot(y = col, data = dados_plot, order=dados_plot[col].value_counts().index)
    ax.set_title(str(col), fontsize = 16)
    ax.set_xlabel('Quantidade', fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel(col, fontsize = 12)
  
    return fig

df_jogadores, df_times = Preproc()

TIMES = df_times.Time.unique()
AGENTES = df_jogadores.Agente.unique()
MAPAS = df_jogadores.Mapa.unique()
ID_PARTIDA = df_times['ID Partida'].unique()

''' # APP VISUALIZAÇÃO DADOS VALORANT'''

##QUAIS FILTROS EU QUERO PARA OS DADOS
# TIMES
# AGENTES
# MAPAS
# "DATA" - POR MATCH_ID. EXPLICAR AS DATAS
# 

filtro_times = st.sidebar.multiselect('Filtro de Times', TIMES)
filtro_agentes = st.sidebar.multiselect('Filtro de Agentes', AGENTES)
filtro_mapas = st.sidebar.multiselect('Filtro de Mapas', MAPAS)
filtro_id = st.sidebar.select_slider('Filtro de Partidas - ID abaixo de 7000 são partidas de 2020', 
                    options=df_times['ID Partida'].unique())

''' ## Dados de Jogadores'''
st.write(df_jogadores.sample(20))



#st.dataframe(jogadores,500,500)

''' ## Dados de Times'''

st.write(df_times.sample(20))

'''### Dados Filtrados'''
filter_df_antigo, filter_df_novo = FilterTimes(df_times, filtro_id, filtro_times, filtro_agentes, filtro_mapas)
st.write(filter_df_antigo)
st.write(filter_df_novo)

#st.dataframe(jogadores)

#graf = st.bar_chart(times.ACS)

categoria_grafico = st.sidebar.selectbox('Selecione a categoria para apresentar no gráfico', options = filter_df_antigo.select_dtypes(include=['object']).columns)
num_obj = st.sidebar.slider('Quantidade de observações do gráfico', 
                            min_value=1, max_value=20)
figura_bar = Countplot(filter_df_antigo, categoria_grafico, num_obj)
st.pyplot(figura_bar)

categoria_grafico = st.sidebar.selectbox('Selecione a categoria para apresentar no gráfico', options = filter_df_antigo.select_dtypes(exclude=['object']).columns)
figura_dist = Distplot(filter_df_antigo, categoria_grafico)
st.pyplot(figura_dist)

