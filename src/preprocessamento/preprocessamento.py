## System
import re
import warnings
from pandas.core import base
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

## EDA
import numpy as np
import pandas as pd
import seaborn as sns
#from pandas_profiling import ProfileReport
pd.set_option('display.max_columns', None)

FILES = ['gamelanders', 'pain', 'vorax', 'havan', 'imperial', 'ingaming', 'vikings', 'black_dragons', 'furia', 'rise', 'slick', 'sharks']
ALL_TEAMS = ['GL', 'IMP','Mix', 'HAVAN', 'HAVA', 'Inga', 'Ingaming', 'NMDM', 'VKS', 'FF', 'VORA', 'BD', 'paiN','NOOR', 'NOORG2.0', 
                'S5', 'Sharks', 'Shar', 'FURI', 'FURIA', 'Rise', 'SLK']

MAPS = ['ASCENT', 'BIND', 'HAVEN', 'ICEBOX', 'SPLIT']

DUELIST = ['jett', 'raze', 'phoenix','reyna', 'yoru']
CONTROLLER = ['omen', 'brimstone', 'viper', 'astra'] 
SENTINEL = ['cypher', 'sage', 'killjoy'] 
INITIATOR = ['breach', 'sova', 'skye']
AGENTS = DUELIST + CONTROLLER + SENTINEL + INITIATOR

NUM_TEAMS = 20

CSV_PATH = '../data/csv/'
EXCEL_PATH = '../data/excel/'


## IMPORT DATA FROM CSV FILE
def ImportData(team_file, type):
    folder = team_file + '/'
    maps_file = team_file + '_'+type+'_MAPS.csv'
    matches_file = team_file + '_'+type+'_MATCHES.csv'
    
    maps = pd.read_csv(CSV_PATH + folder + maps_file)
    matches = pd.read_csv(CSV_PATH + folder + matches_file)

    return maps, matches

## FILTER DATAFRAME BY GIVEN COLUMN ON GIVEN VALUE
def FilterCol(df, col, values):
    return df[df[col].isin(values)].reset_index(drop=True)

def BinaryTarget(variavel, quantil):
  bin = (variavel > variavel.quantile(q = quantil)).astype(int)
  return bin

## Aggregate base_geral by (Team, Match, Map)
def aggBase(base_geral):
    
    mean_agg_cols  = ['ACS', 'K',	'D',	'A',	'KD_DIFF',	'ADR',	'HS%', 'ECON']
    
    sum_agg_cols   = ['FK',	'FD', 'KPR',	'DPR',	'APR',	'FKPR'	,'FDPR',	
                        '2K'	,'3K',	'4K'	,'5K',	
                        '1v1','1v2',	'1v3'	,'1v4'	,'1v5' ,'PL',	'DE', 
                        'total_mult_kill', 'MKPR', 'total_clutch' ,'CPR'] + AGENTS
    
    first_agg_cols = ['Opp_Team_x', 'rounds_won'	,'rounds_lost', 'ct_rounds_won','ct_rounds_lost','t_rounds_won','t_rounds_lost' ,	
                        'total_rounds', 'win_rate', 'ct_wr' , 't_wr', 'RESULT']

    
    '''['Pistol_W','Pistol_P','Pistol_WR' ,'Eco_0_5_P','Eco_0_5_W','Eco_0_5_WR' ,
    'Semi_Eco_5_10_P', 'Semi_Eco_5_10_W','Semi_Eco_5_10_WR', 
    'Semi_Buy_10_20_P','Semi_Buy_10_20_W','Semi_Buy_10_20_WR',
    'Full_Buy_20_P'	,'Full_Buy_20_W','Full_Buy_20_WR']'''

    agg_first = base_geral.groupby(['Team_x','match_id','Map']).first()[first_agg_cols].reset_index()
    agg_sum = base_geral.groupby(['Team_x','match_id','Map']).sum()[sum_agg_cols].reset_index()
    agg_mean = base_geral.groupby(['Team_x','match_id','Map']).mean()[mean_agg_cols].reset_index().round(2)

    merge_agg = agg_mean.merge(agg_sum, how='inner', left_on=['Team_x','match_id','Map'],right_on=['Team_x','match_id','Map']).drop_duplicates()
    merge_agg = merge_agg.merge(agg_first, how='inner', left_on=['Team_x','match_id','Map'],right_on=['Team_x','match_id','Map']).drop_duplicates()

    #merge_agg = merge_agg.merge(economy_maps, how='inner', left_on=['match_id','Map','Team_x'],right_on=['match_id','Map','Team']).drop_duplicates()

    return merge_agg
    
## Get Map data for all teams
def AllTeamsMaps(files, type, team_col, filter_teams):
    concat = pd.concat([ImportData(team_file, type)[0] for team_file in files])
    #filter = FilterCol(concat, team_col, filter_teams)
    filter = concat

    filter[team_col][(filter[team_col] == 'NOOR') | (filter[team_col] == 'NOORG2.0')] = 'paiN'
    filter[team_col][filter[team_col] == 'Mix'] = 'IMP'
    filter[team_col][(filter[team_col] == 'Ingaming') | (filter[team_col] == 'NMDM')] = 'Inga'
    filter[team_col][filter[team_col] == 'FF'] = 'VORA'
    filter[team_col][(filter[team_col] == 'HAVA') | (filter[team_col] == 'HL')] = 'HAVAN'
    filter['Opp_Team'][(filter['Opp_Team'] == 'HAVA') | (filter['Opp_Team'] == 'HL')] = 'HAVAN'
    filter[team_col][filter[team_col] == 'FURI'] = 'FURIA'
    filter[team_col][(filter[team_col] == 'S5') | (filter[team_col] == 'Shar')] = 'Sharks'
    
    
    if type == 'overview': ExtraInfoMaps(filter)
    if type == 'performance':
        # total mult kill + mult kills per round
        filter['total_mult_kill'] = filter.loc[: ,['2K','3K','4K','5K']].sum(axis=1)	

        # total clutches + clutches per round
        filter['total_clutch'] = filter.loc[: ,['1v1','1v2','1v3','1v4','1v5']].sum(axis=1)
    return filter

## Get Match data for all teams
def AllTeamsMatches(files, type, team_col, filter_value):
    concat = pd.concat([ImportData(team_file, type)[1] for team_file in files])
    filter = FilterCol(concat, team_col, filter_value)
    
    filter[team_col][(filter[team_col] == 'NOOR') | (filter[team_col] == 'NOORG2.0')] = 'paiN'
    filter[team_col][filter[team_col] == 'Mix'] = 'IMP'
    filter[team_col][(filter[team_col] == 'Ingaming') | (filter[team_col] == 'NMDM')] = 'Inga'
    filter[team_col][filter[team_col] == 'FF'] = 'VORA'
    filter[team_col][filter[team_col] == 'HAVA'] = 'HAVAN'
    filter[team_col][filter[team_col] == 'FURI'] = 'FURIA'
    filter[team_col][(filter[team_col] == 'S5') | (filter[team_col] == 'Shar')] = 'Sharks'
    
    if type == 'overview': ExtraInfoMatches(filter)
    return filter

## ADD EXTRA INFO TO MATCHES DATAFRAME -- OVERVIEW
def ExtraInfoMatches(df):
    # KDA + FK/FD per map
    df['KPM'] = round(df['K'] / df['Num_maps'],2)
    df['DPM'] = round(df['D'] / df['Num_maps'],2)
    df['APM'] = round(df['A'] / df['Num_maps'],2)
    df['FKPM'] = round(df['FK'] / df['Num_maps'],2)
    df['FDPM'] = round(df['FD'] / df['Num_maps'],2)

## CLUTCH TOTAL, CLUTCH PER ROUND, MULT KILL TOTAL, MULT KILL PER ROUND

## ADD EXTRA INFO TO MAPS DATAFRAME -- OVERVIEW
def ExtraInfoMaps(df):

    # Total Rounds
    df['total_rounds'] = df['rounds_won'] + df['rounds_lost']

    # Round Win Rate
    df['win_rate'] = round(df['rounds_won'] / df['total_rounds'] * 100, 2)

    # KDA + FK/FD per Round
    df['KPR'] = round(df['K'] / df['total_rounds'],2)
    df['DPR'] = round(df['D'] / df['total_rounds'],2)
    df['APR'] = round(df['A'] / df['total_rounds'],2)
    df['FKPR'] = round(df['FK'] / df['total_rounds'],2)
    df['FKWR'] = round(100 * df['FK'] / (df['FK'] + df['FD']), 2)
    df['FDPR'] = round(df['FD'] / df['total_rounds'],2)

    # ATK/DEF Win rate -- ct_rounds_won	ct_rounds_lost	t_rounds_won	t_rounds_lost
    df['ct_wr'] = round(100 * df['ct_rounds_won'] / (df['ct_rounds_won'] + df['ct_rounds_lost']), 2)
    df['t_wr'] = round(100 * df['t_rounds_won'] / (df['t_rounds_won'] + df['t_rounds_lost']), 2)


    # Won/Lost Map 
    df['RESULT'] = ['W' if x == True
                    else 'L'
                    for x in df['rounds_won'] > df['rounds_lost']]

## One Hot Encoding Categorical Cols
def GetDummies(df, cat_cols):

    for col in cat_cols:
        one_hot = pd.get_dummies(df[col])
        #df.drop(col, axis=1, inplace=True)
        df = pd.concat([df, one_hot], axis=1)
    return df

def CompScore(df):

    # jett raze phoenix	reyna yoru	
    # omen brimstone viper astra	
    # cypher sage killjoy 
    # breach	sova	skye

    agro =    [3,3,2,2,2, 1,0,0,0, 0,0,0, 0,0,0]
    tempo =   [0,0,1,1,0, 2,2,1,1, 0,1,0, 3,2,3]
    control = [0,0,0,0,1 ,0,1,2,2, 3,2,3, 0,1,0]

    df['agro_score'] = df[AGENTS].dot(agro)
    df['tempo_score'] = df[AGENTS].dot(tempo)
    df['control_score'] = df[AGENTS].dot(control)

    base_len = df.shape[0]-1
    for idx in range(base_len):
        if idx % 2 == 0:
            df.at[idx, 'opp_agro_score'] = df.at[idx + 1, 'agro_score']
            df.at[idx, 'opp_tempo_score'] = df.at[idx + 1, 'tempo_score']
            df.at[idx, 'opp_control_score'] = df.at[idx + 1, 'control_score']
        else: 
            df.at[idx, 'opp_agro_score'] = df.at[idx - 1, 'agro_score']
            df.at[idx, 'opp_tempo_score'] = df.at[idx - 1, 'tempo_score']
            df.at[idx, 'opp_control_score'] = df.at[idx - 1, 'control_score']
            
    df.at[base_len, 'opp_agro_score'] = df.at[base_len - 1, 'agro_score']
    df.at[base_len, 'opp_tempo_score'] = df.at[base_len - 1, 'tempo_score']
    df.at[base_len, 'opp_control_score'] = df.at[base_len - 1, 'control_score']

    return df


def Preproc():

    overview_maps = AllTeamsMaps(FILES, 'overview', 'Team', ALL_TEAMS)
    performance_maps = AllTeamsMaps(FILES, 'performance', 'Team', ALL_TEAMS)
    #economy_maps = AllTeamsMaps(ALL_FILES, 'economy', 'Team', ALL_TEAMS)

    overview_maps.drop('Patch',axis=1, inplace=True)
    performance_maps.drop('Patch',axis=1, inplace=True)

    base_geral = overview_maps.merge(performance_maps, 
                                    how='inner', 
                                    left_on=['match_id','Map','Player'],
                                    right_on=['match_id','Map','Player']).drop_duplicates()
    #base_geral = merge_over_perf.merge(economy_maps, how='inner', left_on=['match_id','Map','Team_x'],right_on=['match_id','Map','Team']).drop_duplicates()

    # Filter data using most frequent teams
    top_teams = list(base_geral['Team_x'].value_counts()[:NUM_TEAMS].index)
    base_geral = base_geral[base_geral['Team_x'].isin(top_teams)]

    # Replace Null values and create new features
    base_geral = base_geral.replace(np.nan, 0)
    base_geral = GetDummies(base_geral, ['Agents'])
    base_geral['MKPR'] = round(base_geral['total_mult_kill'] / base_geral['total_rounds'], 2)
    base_geral['CPR'] = round(base_geral['total_clutch'] / base_geral['total_rounds'], 2)
    base_geral = base_geral[base_geral.match_id != 16846]

    # Aggregate data by Team-Match-Map
    base_agg = aggBase(base_geral)
    base_agg = base_agg.replace(np.nan, 0)
    base_agg[AGENTS] = base_agg[AGENTS].replace(2, 1)
    base_agg = base_agg[base_agg.FKPR < 1]
    base_agg.RESULT = base_agg.RESULT.replace({'W':'Vitoria', 'L': 'Derrota'})
    base_agg = base_agg.sort_values(['match_id', 'Map']).reset_index(drop=True)
    base_agg = base_agg.drop(780,axis=0).reset_index(drop=True)

    # Create composition scores for Agro, Tempo and Control Compositios
    base_agg = CompScore(base_agg)
    
    # Select and rename final columns
    features_keep_players = ['Player', 'Agents','ACS', 'K',               'D',               'A',
               'KD_DIFF',             'ADR',             'HS%',
                    'FK',              'FD',      'FK_FD_DIFF', 'match_id', 'Map',
                    'KPR',             'DPR',             'APR',
                    'FKPR',            'FKWR',            'FDPR',
                    '2K',              '3K',              '4K',
                    '5K',             '1v1',             '1v2',
                   '1v3',             '1v4',             '1v5',
                  'ECON',              'PL',              'DE',
                  'total_mult_kill','total_clutch', 'MKPR',
                   'CPR']
    base_geral = base_geral[features_keep_players]
    base_geral.columns = [
    'Jogador', 'Agente', 'ACS', 
    'Kills', 'Deaths', 'Assists',
    'Diferenca Kill/Death','ADR', 'HS%',
    'First Kills', 'First Deaths', 'Diferenca FK/FD',
    'ID Partida', 'Mapa','Kills Por Round', 'Deaths Por Round','Assists Por Round',
    'First Kill Por Round', 'Win Rate First Kills', 'First Death Por Round',
    'Double Kills', 'Triple Kills', 'Quadra Kills', 'Penta Kills',
    '1v1', '1v2', '1v3', '1v4', '1v5','Nota Economia', 'Plants', 'Defuses',
    'Total Mult Kills', 'Total Clutches', 'Clutches Por Round','Mult Kills Por Round']

    feat_keep_teams = [
    'Team_x', 'match_id', 'Map', 'ACS', 
    'K', 'D', 'A', 'KD_DIFF', 'ADR',
    'HS%', 'ECON', 'FK', 'FD', 'KPR', 
    'DPR', 'APR', 'FKPR', 'FDPR', '2K',
    '3K', '4K', '5K', '1v1', '1v2', 
    '1v3', '1v4', '1v5', 'PL', 'DE',
    'total_mult_kill', 'MKPR', 'total_clutch', 'CPR', 'Opp_Team_x', 'rounds_won', 
    'rounds_lost', 'ct_rounds_won', 'ct_rounds_lost','t_rounds_won', 't_rounds_lost', 
    'total_rounds', 'win_rate', 'ct_wr', 't_wr', 'RESULT', 
    'agro_score', 'tempo_score', 'control_score', 
    'opp_agro_score', 'opp_tempo_score', 'opp_control_score']

    base_agg = base_agg[feat_keep_teams]

    base_agg.columns=[
    'Time', 'ID Partida', 'Mapa', 'ACS', 
    'Kills', 'Deaths', 'Assists','Diferenca Kill/Death', 'ADR', 
    'HS%', 'Nota Economia','First Kills', 'First Deaths', 'Kills Por Round', 
    'Deaths Por Round','Assists Por Round', 'First Kill Por Round', 'First Death Por Round','Double Kills', 
    'Triple Kills', 'Quadra Kills', 'Penta Kills', '1v1', '1v2', 
    '1v3', '1v4', '1v5', 'Plants', 'Defuses', 
    'Total Mult Kills', 'Mult Kills Por Round', 'Total Clutches','Clutches Por Round', 'Time Oponente', 'Rounds Vencidos',
    'Rounds Perdidos', 'Vitorias DEF', 'Derrotas DEF', 'Vitorias ATK', 'Derrotas ATK',
    'Rounds Totais', 'Win Rate', 'Win Rate DEF', 'Win Rate ATK', 'Resultado',
    'Score Comp Agro', 'Score Comp Tempo', 'Score Comp Control',
    'Score Comp Agro Oponente', 'Score Comp Tempo Oponente','Score Comp Control Oponente'] 

    return base_geral, base_agg

