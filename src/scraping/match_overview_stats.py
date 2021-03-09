#!/usr/bin/python3
import pandas as pd
import numpy as np 
import re

import urllib
from urllib.request import urlopen as uReq

from scraping.match_utils import GetMaps, GetAgents, GetPatchVer, Scores, SideScores

MATCH_OVERVIEW_SUFIX = '?game=all&tab=overview'

## Match Overall Stats
## Concats Info from Match Info + Each Map (1-5 Maps)
def MatchOverviewStats(match_url):

  df_match = None

  try:
    df_match = pd.read_html(match_url + MATCH_OVERVIEW_SUFIX)
  except:
    print("** DATA FRAME READ ERROR -- " + str(match_url) + " **")
    return None

  match_cols = ['Player', 'Agents', 'ACS',	'K',	'D',	'A',	
                'KD_DIFF',	'ADR',	'HS%',	'FK',	'FD',	'FK_FD_DIFF']
  
  try:
    client = uReq(match_url)
    page_html = client.read()
    client.close()
  except:
    print("HTTP Error 404: " + str(match_url) + " Not Found")
    return None
  
  match_maps, map_adv = GetMaps(page_html)
  agents = GetAgents(page_html)
  rounds_won = Scores(page_html)
  patch = GetPatchVer(page_html)
  scores_t, scores_ct  = SideScores(page_html)
  match_id = match_url.split('/')[3]
  df_match = [df for df in df_match if df.isnull().sum().sum() < 6]

  for df in df_match:
    if df.isnull().sum().sum() < 6:
      df.columns = match_cols
      df['match_id'] = match_id
      df['Team'] = None
      df['Team'] = [x.split(' ')[-1]
                    if len(x.split(' ')) > 1
                    else x.split(' ')[-1]
                    for x in df['Player'] ]

      df['Player'] = [ x.split(' ')[0] for x in df['Player'] ]
      
      df['D'] = [int(''.join(filter(str.isdigit, x))) 
                if len(x) > 0
                else ' ' 
                for x in  df['D']]

      df['HS%'] = [int(''.join(filter(str.isdigit, x))) 
                  if len(x) > 0
                  else ' ' 
                  for x in  df['HS%']]
 
  return ConcatMaps(df_match, match_maps, map_adv, agents, rounds_won, patch, scores_t, scores_ct) 

## Add new columns on map dataframe
def AddInfoMap(df, map, agents, rounds_w, rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t):
  
  df[['Opp_Team', 'rounds_won', 'rounds_lost', 
      'ct_rounds_won', 'ct_rounds_lost', 't_rounds_won', 't_rounds_lost']] = None

  df['Agents'] = agents
  df['Opp_Team'][0:5] = df['Team'][9] 
  df['Opp_Team'][5:10] = df['Team'][0]
  df['Map'] = map
  
  ## Team 1                          
  df['rounds_won'][0:5] = rounds_w 
  df['rounds_lost'][0:5] = rounds_l
  df['ct_rounds_won'][0:5] = t1_ct
  df['ct_rounds_lost'][0:5] = t2_t
  df['t_rounds_won'][0:5] = t1_t
  df['t_rounds_lost'][0:5] = t2_ct

  ## Team 2
  df['rounds_lost'][5:10] = rounds_w
  df['rounds_won'][5:10] = rounds_l
  df['ct_rounds_won'][5:10] = t2_ct
  df['ct_rounds_lost'][5:10] = t1_t
  df['t_rounds_won'][5:10] = t2_t
  df['t_rounds_lost'][5:10] = t1_ct

  df['Patch'] = patch

  return df

## Concat Tables for each map - Based on number of maps on the Match
## Create column for opponent team
## Fill Agents Column
def ConcatMaps(df_match, match_maps, map_adv, agents, round_won, patch, scores_t, scores_ct):
  
  if map_adv: round_won = round_won[2:]
  t1_rounds_w = round_won[0]
  t1_rounds_l = round_won[1]
  t1_ct = scores_ct[0]
  t1_t = scores_t[0]
  t2_ct = scores_ct[1]
  t2_t = scores_t[1]

  if len(match_maps) > 0: map = match_maps[0]
  else: map = 'N/A'
  if map_adv: agents = agents[10:]

  n_maps = int((len(df_match) - 2) / 2)
  
  ## 1 MAP
  if map_adv == 0:
    df_map1 = pd.concat(df_match[:2], ignore_index=True)
    df_map1 = AddInfoMap(df_map1, map, agents[:10], 
                       t1_rounds_w, t1_rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t)
  else:
    df_map1 = pd.concat(df_match[2:4], ignore_index=True)
    df_map1 = AddInfoMap(df_map1, map, agents[10:20], 
                       t1_rounds_w, t1_rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t)

  ## 2 MAPS
  if n_maps > 1:
    t1_rounds_w = round_won[2]
    t1_rounds_l = round_won[3]
    t1_ct = scores_ct[2]
    t1_t = scores_t[2]
    t2_ct = scores_ct[3]
    t2_t = scores_t[3]
    map = match_maps[1]
    df_map2 = pd.concat(df_match[4:6], ignore_index=True)
    df_map2 = AddInfoMap(df_map2, map, agents[20:30], 
                          t1_rounds_w, t1_rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t)
  else: df_map2 = None
  
  ## 3 MAPS
  if n_maps > 2:
    t1_rounds_w = round_won[4]
    t1_rounds_l = round_won[5]
    t1_ct = scores_ct[4]
    t1_t = scores_t[4]
    t2_ct = scores_ct[5]
    t2_t = scores_t[5]
    map = match_maps[2]
    df_map3 = pd.concat(df_match[6:8], ignore_index=True)
    df_map3 = AddInfoMap(df_map3, map, agents[30:40], 
                         t1_rounds_w, t1_rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t)
  else: df_map3 = None

  ## 4 MAPS
  if n_maps > 3:
    t1_rounds_w = round_won[6]
    t1_rounds_l = round_won[7]
    t1_ct = scores_ct[6]
    t1_t = scores_t[5]
    t2_ct = scores_ct[7]
    t2_t = scores_t[7]
    map = match_maps[3]
    df_map4 = pd.concat(df_match[8:10], ignore_index=True)
    df_map4 = AddInfoMap(df_map4, map, agents[40:50], 
                          t1_rounds_w, t1_rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t)    
  else: df_map4 = None

  ## 5 MAPS
  if n_maps > 4:
     t1_rounds_w = round_won[8]
     t1_rounds_l = round_won[9]
     t1_ct = scores_ct[8]
     t1_t = scores_t[8]
     t2_ct = scores_ct[9]
     t2_t = scores_t[9]
     map = match_maps[3]
     map = match_maps[4]
     df_map5 = pd.concat(df_match[10:12], ignore_index=True)
     df_map5 = AddInfoMap(df_map5, map, agents[50:60], 
                          t1_rounds_w, t1_rounds_l, patch, t1_ct, t1_t, t2_ct, t2_t)
  else: df_map5 = None

  if map_adv == 0: df_all_maps = pd.concat(df_match[2:4], ignore_index=True)
  else: df_all_maps = pd.concat(df_match[:2], ignore_index=True)
  
  df_all_maps['Opp_Team'] = None
  df_all_maps['Opp_Team'][0:5] = df_all_maps['Team'][9]
  df_all_maps['Opp_Team'][5:10] = df_all_maps['Team'][0]
  df_all_maps['Map'] = 'MATCH'
  df_all_maps['Num_maps'] = n_maps
  df_all_maps['Patch'] = patch
  df_all_maps.drop('Agents',axis=1, inplace=True)

  return [df_all_maps, df_map1, df_map2, df_map3, df_map4, df_map5]
