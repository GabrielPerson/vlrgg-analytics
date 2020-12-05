'''## Web Scraping
import bs4
from bs4 import BeautifulSoup as soup
import urllib
from urllib.request import urlopen as uReq

import pandas as pd 


MAPS = ['Haven', 'Bind', 'Split', 'Ascent', 'Icebox']

## Retrieve Match Map names
def GetMaps(url_match):

  map_list = []

  client = uReq(url_match)
  page_html = client.read()
  client.close()

  page_soup = soup(page_html,"html.parser")
  div_maps = page_soup.find("div",{"class":"vm-stats-gamesnav-container"})
  map_src = div_maps.findAll("div", {"style":"margin-bottom: 2px; text-align: center; line-height: 1.5;"})

  # Get map if match is a best of 1
  if len(map_src) == 0:
    div_map_bo1 = page_soup.find("div",{"class":"map"})
    if div_map_bo1 is None: 
      return None
    else:
      map_bo1 = div_map_bo1.findAll("div", {"style":"font-weight: 700; font-size: 20px; text-align: center; position: relative;"})
      for src in map_bo1:
        for x in MAPS:
          if x in str(src):
            map_list.append(x.upper())
    return map_list

  for src in map_src:
    for x in MAPS:
      if x in str(src):
        map_list.append(x.upper())
  
  return map_list

## Match Overall Stats
## Concats Info from Match Info + Each Map (1-5 Maps)
def MatchOverallStats(match_over_url):

  df_match = pd.read_html(match_over_url)
  match_cols = ['Player', 'Agents', 'ACS',	'K',	'D',	'A',	'KD_DIFF',	'ADR',	'HS%',	'FK',	'FD',	'FK_FD_DIFF']
  match_maps = ['ALL'] + GetMaps(match_over_url)

  for df in df_match:
    df.columns = match_cols
    df['Team'] = [x.split(' ')[-1]
                  if len(x.split(' ')) > 1
                  else x.split(' ')[-1]
                  for x in df['Player'] ]
    df['Player'] = [ x.split(' ')[0] for x in df['Player'] ]
    
    df['D'] = [int(''.join(filter(str.isdigit, x))) for x in  df['D']]

    df['HS%'] = [int(''.join(filter(str.isdigit, x))) for x in  df['HS%']]

    df.drop('Agents',axis=1, inplace=True)

  return ConcatMaps(df_match, match_maps) 

## Concat Tables for each map - Based on number of maps on the Match
## Create column for opponent team
def ConcatMaps(df_match, match_maps):
  
  df_map1 = pd.concat(df_match[:2], ignore_index=True)
  df_map1['Map'] = match_maps[1]
  df_map1['Opp_Team'] = None
  df_map1['Opp_Team'][0:5] = df_map1['Team'][9]
  df_map1['Opp_Team'][5:10] = df_map1['Team'][0]
  
  if len(df_match) > 4: 
    df_map2 = pd.concat(df_match[4:6], ignore_index=True)
    df_map2['Map'] = match_maps[2]
    df_map2['Opp_Team'] = None
    df_map2['Opp_Team'][0:5] = df_map2['Team'][9]
    df_map2['Opp_Team'][5:10] = df_map2['Team'][0]
  else: df_map2 = None
  
  if len(df_match) > 6:
     df_map3 = pd.concat(df_match[6:8], ignore_index=True)
     df_map3['Map'] = match_maps[3]
     df_map3['Opp_Team'] = None
     df_map3['Opp_Team'][0:5] = df_map3['Team'][9]
     df_map3['Opp_Team'][5:10] = df_map3['Team'][0]
  else: df_map3 = None
  
  df_all_maps = pd.concat(df_match[2:4], ignore_index=True)
  df_all_maps['Map'] = match_maps[0]
  df_all_maps['Opp_Team'] = None
  df_all_maps['Opp_Team'][0:5] = df_all_maps['Team'][9]
  df_all_maps['Opp_Team'][5:10] = df_all_maps['Team'][0]

  return [df_all_maps, df_map1, df_map2, df_map3]

## Player perfomance from match + each map
def MatchPerfStats(match_url):
  
  df = pd.read_html(match_url)

  df_matchup_all = df[:3]
  df_matchup_all = MatchUpKills(df_matchup_all)

  df_mk_clutch_all = df[3]
  df_mk_clutch_all = MultKCluth(df_mk_clutch_all)

  return [df_matchup_all, df_mk_clutch_all]

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
def MultKCluth(df):
  
  df.columns = ['Player', 'drop'] + list(df.columns[2:])
  df.drop('drop',axis=1, inplace= True)

  df['Team'] = [x.split()[1] for x in df['Player']]
  df['Player'] = [x.split()[0] for x in df['Player']]

  stats_cols = ['2K', '3K', '4K'  ,'5K' ,'1v1', '1v2',  '1v3',  '1v4',  '1v5']
  for idx in  df.index:
    for col in stats_cols:
      if pd.isna(df.at[idx, col]): df.at[idx, col] = 0

  df['Opp_Team'] = None
  df['Opp_Team'][0:5] = df['Team'][9]
  df['Opp_Team'][5:10] = df['Team'][0]

  return df                     

## Clean Economy Stats
## Create Win, Played, WinRate columns for each Buy Type
## Create Opp Team column
## Create number of maps column
def CleanEconStats(df_econ_all):
  
  econ_cols = ['Team', 'Pistol_W', 'Eco', 'Semi_Eco: 0-5', 'Semi_Buy: 10-20', 'Full_Buy: +20']
  df_econ_all.columns = econ_cols
  
  df_econ_all['Pistol_P'] = df_econ_all['Pistol_W'][0] + df_econ_all['Pistol_W'][1] 
  df_econ_all['Pistol_P'] = df_econ_all['Pistol_W'][0] + df_econ_all['Pistol_W'][1]
  df_econ_all['Pistol_WR'] = round(df_econ_all['Pistol_W'] / df_econ_all['Pistol_P'] * 100,0)

  df_econ_all['Eco_P'] = [int(''.join(filter(str.isdigit, x.split()[0]))) for x in df_econ_all['Eco']]  
  df_econ_all['Eco_W'] = [int(''.join(filter(str.isdigit, x.split()[1]))) for x in df_econ_all['Eco']]
  df_econ_all['Eco_WR'] = round(df_econ_all['Eco_W'] / df_econ_all['Eco_P'] * 100,0)

  df_econ_all['Semi_Eco_0_5_P'] = [int(''.join(filter(str.isdigit, x.split()[0]))) for x in df_econ_all['Semi_Eco: 0-5']]  
  df_econ_all['Semi_Eco_0_5_W'] = [int(''.join(filter(str.isdigit, x.split()[1]))) for x in df_econ_all['Semi_Eco: 0-5']]
  df_econ_all['Semi_Eco_0_5_WR'] = round(df_econ_all['Semi_Eco_0_5_W'] / df_econ_all['Semi_Eco_0_5_P'] * 100,0)

  df_econ_all['Semi_Buy_10_20_P'] = [int(''.join(filter(str.isdigit, x.split()[0]))) for x in df_econ_all['Semi_Buy: 10-20']]  
  df_econ_all['Semi_Buy_10_20_W'] = [int(''.join(filter(str.isdigit, x.split()[1]))) for x in df_econ_all['Semi_Buy: 10-20']]
  df_econ_all['Semi_Buy_10_20_WR'] = round(df_econ_all['Semi_Buy_10_20_W'] / df_econ_all['Semi_Buy_10_20_P'] * 100,0)

  df_econ_all['Full_Buy_20_P'] = [int(''.join(filter(str.isdigit, x.split()[0]))) for x in df_econ_all['Full_Buy: +20']]  
  df_econ_all['Full_Buy_20_W'] = [int(''.join(filter(str.isdigit, x.split()[1]))) for x in df_econ_all['Full_Buy: +20']]
  df_econ_all['Full_Buy_20_WR'] = round(df_econ_all['Full_Buy_20_W'] / df_econ_all['Full_Buy_20_P'] * 100 ,0)

  df_econ_all['Opp_team'] = [df_econ_all['Team'][1], df_econ_all['Team'][0]]
  df_econ_all['Num_maps'] = df_econ_all['Pistol_P'] / 2

  df_econ_all.drop(['Eco', 'Semi_Eco: 0-5', 'Semi_Buy: 10-20', 'Full_Buy: +20'], axis=1, inplace=True)

  return df_econ_all

## Get Match Economy Sats
def MatchEconStats(match_url):
  
  match_econ_maps = GetMaps(match_url)
  df_econ = pd.read_html(match_url)

  all_econ_stats = CleanEconStats(df_econ[-1])

  if match_econ_maps is None: 
    return all_econ_stats
  else:
    map_econ_stats = [CleanEconStats(df_econ[x*2]) for x in range(len(match_econ_maps))]
    for x in range(len(match_econ_maps)):
      map_econ_stats[x]['Map'] = match_econ_maps[x]

  return [all_econ_stats, map_econ_stats]'''