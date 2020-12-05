import pandas as pd
import numpy as np 
import re

from match_utils import GetMaps
from match_utils import GetPatchVer
from match_utils import GetAgents
from match_utils import Scores


## Player perfomance from match + each map
def MatchPerfStats(match_url):
  
  try:
    df = pd.read_html(match_url + MATCH_PERFORMANCE_SUFIX)
  except:
    print("** DATA FRAME READ ERROR **")
  
  maps, map_adv = GetMaps(match_url)
  patch = GetPatchVer(match_url)
  n_maps = int((len(df) / 4)-1)

  #df_matchup_all = MatchUpKills(df[:3])
  df_matchup_all = None

  df_mk_clutch_all = MultKCluth(df[3], None, patch)
  df_mk_clutch_all['Map'] = 'MATCH'
  df_mk_clutch_all['Num_maps'] = n_maps
  
  mk_clutch_maps = None
  if n_maps > 0:
    mk_clutch_maps = [MultKCluth(df[3 + ((x+1)*4)], maps[x], patch) for x in range(n_maps)]

  return [df_matchup_all, df_mk_clutch_all, mk_clutch_maps]

## Matchup kills from each player duel (Player x Player)
def MatchUpKills(df_list):

  matchup_kills = {}
  dict_idx = ['all_k', 'first_k', 'op_k']
  idx_ct = 0

  for x in dict_idx:
    matchup_kills[x] = None

  for df in df_list:
    df.columns = [0] + [x.split()[0] for x in df.iloc[0][1:]]
    df.drop(0, axis=0, inplace=True)
    df.index = [x.split()[0] for x in df[0]]
    df.drop(0, axis=1, inplace=True)

    for idx in df.index:
      for col in df.columns:
        if pd.isna(df.at[idx, col]): df.at[idx, col] = [0, 0, 0]
        else:
          df.at[idx, col] = [int(''.join(filter(str.isdigit, x))) * -1
                            if x[0] == '-' 
                            else int(''.join(filter(str.isdigit, x)))
                            for x in df.at[idx, col].split()]
    
    matchup_kills[dict_idx[idx_ct]] = MirrorMatchUp(df)
    idx_ct += 1

  return matchup_kills   

## Expand MatchUp Data Frame to mirror player match ups
def MirrorMatchUp(df):
  
  add_df = pd.DataFrame(0, index = list(df.columns) , columns = list(df.columns) + list(df.index))
  df[list(df.index)] = 0
  
  exp_df = df.append(add_df)
  
  exp_df[list(df.columns)] = exp_df[list(df.columns)].astype(object)
  for idx in list(exp_df.index):
    for col in list(exp_df.columns):
      if exp_df.at[idx, col] != 0:
        exp_df.loc[col, idx] = [None] * 3
        exp_df.at[col, idx][0] = exp_df.at[idx, col][1]
        exp_df.at[col, idx][1] = exp_df.at[idx, col][0]
        exp_df.at[col, idx][2] = exp_df.at[idx, col][2] * -1
  
  return exp_df

## Get Mult Kill and Clutch (1vX) data for each player
def MultKCluth(df, map, patch):