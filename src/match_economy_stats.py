#!/usr/bin/python3
import pandas as pd
import numpy as np 
import re
import warnings

from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

from match_utils import GetMaps, GetAgents, GetPatchVer, Scores

MATCH_ECON_SUFIX = '?game=all&tab=economy'

## Clean Economy Stats
## Create Win, Played, WinRate columns for each Buy Type
## Create Opp Team column
## Create number of maps column
def CleanEconStats(df_econ_all, patch):
  
  econ_cols = ['Team', 'Pistol_W', 'Eco', 'Semi_Eco: 5-10', 'Semi_Buy: 10-20', 'Full_Buy: +20']
  df_econ_all.columns = econ_cols
  
  df_econ_all['Pistol_P'] = df_econ_all['Pistol_W'][0] + df_econ_all['Pistol_W'][1] 
  df_econ_all['Pistol_P'] = df_econ_all['Pistol_W'][0] + df_econ_all['Pistol_W'][1]
  df_econ_all['Pistol_WR'] = round(df_econ_all['Pistol_W'] / df_econ_all['Pistol_P'] * 100,0)

  df_econ_all['Eco_0_5_P'] = [int(''.join(filter(str.isdigit, x.split()[0]))) for x in df_econ_all['Eco']]  
  df_econ_all['Eco_0_5_W'] = [int(''.join(filter(str.isdigit, x.split()[1]))) for x in df_econ_all['Eco']]
  df_econ_all['Eco_0_5_WR'] = round(df_econ_all['Eco_0_5_W'] / df_econ_all['Eco_0_5_P'] * 100,0)

  df_econ_all['Semi_Eco_5_10_P'] = [int(''.join(filter(str.isdigit, x.split()[0]))) for x in df_econ_all['Semi_Eco: 5-10']]  
  df_econ_all['Semi_Eco_5_10_W'] = [int(''.join(filter(str.isdigit, x.split()[1]))) for x in df_econ_all['Semi_Eco: 5-10']]
  df_econ_all['Semi_Eco_5_10_WR'] = round(df_econ_all['Semi_Eco_5_10_W'] / df_econ_all['Semi_Eco_5_10_P'] * 100,0)

  df_econ_all['Semi_Buy_10_20_P'] = [int(''.join(filter(str.isdigit, x.split()[0]))) for x in df_econ_all['Semi_Buy: 10-20']]  
  df_econ_all['Semi_Buy_10_20_W'] = [int(''.join(filter(str.isdigit, x.split()[1]))) for x in df_econ_all['Semi_Buy: 10-20']]
  df_econ_all['Semi_Buy_10_20_WR'] = round(df_econ_all['Semi_Buy_10_20_W'] / df_econ_all['Semi_Buy_10_20_P'] * 100,0)

  df_econ_all['Full_Buy_20_P'] = [int(''.join(filter(str.isdigit, x.split()[0]))) for x in df_econ_all['Full_Buy: +20']]  
  df_econ_all['Full_Buy_20_W'] = [int(''.join(filter(str.isdigit, x.split()[1]))) for x in df_econ_all['Full_Buy: +20']]
  df_econ_all['Full_Buy_20_WR'] = round(df_econ_all['Full_Buy_20_W'] / df_econ_all['Full_Buy_20_P'] * 100 ,0)

  df_econ_all['Opp_team'] = [df_econ_all['Team'][1], df_econ_all['Team'][0]]
  df_econ_all['Num_maps'] = df_econ_all['Pistol_P'] / 2
  df_econ_all['Patch'] = patch

  df_econ_all.drop(['Eco', 'Semi_Eco: 5-10', 'Semi_Buy: 10-20', 'Full_Buy: +20'], axis=1, inplace=True)

  return df_econ_all

## Get Match Economy Sats
def MatchEconStats(match_url):
  
  try:
    df_econ = pd.read_html(match_url + MATCH_ECON_SUFIX)
  except:
    print("** DATA FRAME READ ERROR **")
  
  patch = GetPatchVer(match_url)

  maps, _ = GetMaps(match_url)
  all_econ_stats = CleanEconStats(df_econ[-1], patch)
  all_econ_stats['Map'] = 'MATCH'
  n_maps = int(all_econ_stats['Num_maps'][0]) 

  ## Case BO1
  if n_maps == 1: 
    map_econ_stats = all_econ_stats.copy()
    map_econ_stats['Map'] = maps[0]
    return [all_econ_stats, [map_econ_stats]]

  if maps is None: 
    return all_econ_stats
  else:
    map_econ_stats = [CleanEconStats(df_econ[x*2], patch) for x in range(n_maps)]
    for x in range(n_maps):
      map_econ_stats[x]['Map'] = maps[x]

  return [all_econ_stats, map_econ_stats]