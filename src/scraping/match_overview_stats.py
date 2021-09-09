#!/usr/bin/python3
import pandas as pd
from urllib.request import urlopen as uReq

from scraping.match_utils import GetMaps, GetAgents, GetPatchVer, Scores, SideScores

MATCH_OVERVIEW_SUFIX = '?game=all&tab=overview'

## Match Overall Stats
## Concats Info from Match Info + Each Map (1-5 Maps)
def MatchOverviewStats(match_url: str) -> list():

  df_match = None

  # CHECK DATAFRAME ERROR EXCEPTION
  try:
    df_match = pd.read_html(match_url + MATCH_OVERVIEW_SUFIX)
  except:
    print("** DATA FRAME READ ERROR -- " + str(match_url) + " **")
    return None

  # CHECK 404 EXCEPTION
  try:
    client = uReq(match_url)
    page_html = client.read()
    client.close()
  except:
    print("HTTP Error 404: " + str(match_url) + " Not Found")
    return None
  
  match_cols = ['Player', 'Agents', 'ACS',	'K',	'D',	'A',	
                'KD_DIFF',	'ADR',	'HS%',	'FK',	'FD',	'FK_FD_DIFF']

  
  match_maps, map_adv = GetMaps(page_html)
  agents = GetAgents(page_html)
  rounds_won = Scores(page_html)
  patch = None #GetPatchVer(page_html)
  scores_atk, scores_def  = SideScores(page_html)
  match_id = match_url.split('/')[3]

  # Remove MATCH df
  if map_adv: del df_match[:2]
  else: del df_match[2:4]

  # Filter DFs with not enough data
  df_match = [df for df in df_match if df.isnull().sum().sum() < 6]
  df_match = [df for df in df_match if len(df.index) > 0]
  if len(df_match) < 1: return None

  for df in df_match:
    df.columns = match_cols
    df['match_id'] = match_id
    df['Team'] = None
    df['Team'] = [x.split(' ')[-1]
                  if len(x.split(' ')) > 1
                  else x.split(' ')[-1]
                  for x in df['Player'] ]

    df['Player'] = [ x.split(' ')[0] for x in df['Player'] ]
    
    df['D'] = [int(''.join(filter(str.isdigit, x))) 
              if len(str(x)) > 0
              else ' ' 
              for x in list(df['D'])]

    df['HS%'] = [int(''.join(filter(str.isdigit, x))) 
                if len(str(x)) > 0
                else ' ' 
                for x in list(df['HS%'])]
 
  return ConcatMaps(df_match, match_maps, map_adv, agents, rounds_won, patch, scores_atk, scores_def) 

## Add new columns on map dataframe
def AddInfoMap(df: pd.DataFrame, map: str, agents: list, 
              rounds_w: int, rounds_l: int, patch: float, 
              t1_ct: int, t1_t:int, 
              t2_ct:int, t2_t:int) -> pd.DataFrame():
  
  df[['Opp_Team', 'rounds_won', 'rounds_lost', 
      'ct_rounds_won', 'ct_rounds_lost', 't_rounds_won', 't_rounds_lost']] = None

  df['Agents'] = pd.Series(agents)
  df['Opp_Team'][:5] = df['Team'].iloc[-1]
  df['Opp_Team'][5:] = df['Team'].iloc[0]
  df['Map'] = map
  
  ## Team 1                          
  df['rounds_won'][:5] = rounds_w 
  df['rounds_lost'][:5] = rounds_l
  df['ct_rounds_won'][:5] = t1_ct
  df['ct_rounds_lost'][:5] = t2_t
  df['t_rounds_won'][:5] = t1_t
  df['t_rounds_lost'][:5] = t2_ct

  ## Team 2
  df['rounds_lost'][5:] = rounds_w
  df['rounds_won'][5:] = rounds_l
  df['ct_rounds_won'][5:] = t2_ct
  df['ct_rounds_lost'][5:] = t1_t
  df['t_rounds_won'][5:] = t2_t
  df['t_rounds_lost'][5:] = t1_ct

  df['Patch'] = patch

  return df

## Concat Tables for each map - Based on number of maps on the Match
## Create column for opponent team
## Fill Agents Column
def ConcatMaps(df_match:pd.DataFrame, match_maps:list, map_adv:int, 
              agents:list, round_won:list, patch:float, 
              scores_atk:list, scores_def:list) -> list():
  

  if map_adv: round_won = round_won[2:]
  if round_won is not None:
    t1_rounds_w = round_won[0]
    t1_rounds_l = round_won[1]
  if (len(scores_def) > 0) & (len(scores_atk) > 0):
    t1_def = scores_def[0]
    t1_atk = scores_atk[0]
    t2_def = scores_def[1]
    t2_atk = scores_atk[1]
  else: t1_def = t2_def = t1_atk = t2_atk = 0

  if len(match_maps) > 0: map = match_maps[0]
  else: map = 'N/A'

  if map_adv: agents = agents[20:]
  else: del agents[10:20]

  n_maps = int(len(df_match) / 2)
  
  ## 1 MAP
  df_map1 = pd.concat(df_match[:2], ignore_index=True)
  df_map1 = AddInfoMap(df_map1, map, agents[:10], 
                       t1_rounds_w, t1_rounds_l, patch, 
                       t1_def, t1_atk, t2_def, t2_atk)
  '''
  if map_adv == 0:
    df_map1 = AddInfoMap(df_map1, map, agents[:10], 
                       t1_rounds_w, t1_rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t)
  else:
    #df_map1 = pd.concat(df_match[2:4], ignore_index=True)
    df_map1 = AddInfoMap(df_map1, map, agents[10:20], 
                       t1_rounds_w, t1_rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t)
  '''

  ## 2 MAPS
  if n_maps > 1:
    t1_rounds_w = round_won[2]
    t1_rounds_l = round_won[3]
    t1_def = scores_def[2]
    t1_atk = scores_atk[2]
    t2_def = scores_def[3]
    t2_atk = scores_atk[3]
    map = match_maps[1]
    df_map2 = pd.concat(df_match[2:4], ignore_index=True)
    df_map2 = AddInfoMap(df_map2, map, agents[10:20], 
                          t1_rounds_w, t1_rounds_l, patch, 
                          t1_def, t1_atk, t2_def, t2_atk)
  else: df_map2 = None
  
  ## 3 MAPS
  if n_maps > 2:
    t1_rounds_w = round_won[4]
    t1_rounds_l = round_won[5]
    t1_def = scores_def[4]
    t1_atk = scores_atk[4]
    t2_def = scores_def[5]
    t2_atk = scores_atk[5]
    map = match_maps[2]
    df_map3 = pd.concat(df_match[4:6], ignore_index=True)
    df_map3 = AddInfoMap(df_map3, map, agents[20:30], 
                         t1_rounds_w, t1_rounds_l, patch, 
                         t1_def, t1_atk, t2_def, t2_atk)
  else: df_map3 = None

  ## 4 MAPS
  if n_maps > 3:
    t1_rounds_w = round_won[6]
    t1_rounds_l = round_won[7]
    t1_def = scores_def[6]
    t1_atk = scores_atk[5]
    t2_def = scores_def[7]
    t2_atk = scores_atk[7]
    map = match_maps[3]
    df_map4 = pd.concat(df_match[6:8], ignore_index=True)
    df_map4 = AddInfoMap(df_map4, map, agents[30:40], 
                          t1_rounds_w, t1_rounds_l, patch, 
                          t1_def, t1_atk, t2_def, t2_atk)    
  else: df_map4 = None

  ## 5 MAPS
  if n_maps > 4:
     t1_rounds_w = round_won[8]
     t1_rounds_l = round_won[9]
     t1_def = scores_def[8]
     t1_atk = scores_atk[8]
     t2_def = scores_def[9]
     t2_atk = scores_atk[9]
     map = match_maps[4]
     df_map5 = pd.concat(df_match[8:10], ignore_index=True)
     df_map5 = AddInfoMap(df_map5, map, agents[40:50], 
                          t1_rounds_w, t1_rounds_l, patch, 
                          t1_def, t1_atk, t2_def, t2_atk)
  else: df_map5 = None

  df_all_maps = None

  return [df_all_maps, df_map1, df_map2, df_map3, df_map4, df_map5]
