#!/usr/bin/python3
import pandas as pd
from pandas.core.common import SettingWithCopyWarning

## Get and Clean Team Map Stats
def TeamMapStats(team_url: str) -> pd.DataFrame:
  
  try:
    df = pd.read_html(team_url)[0]
  except:
    print("** DATA FRAME READ ERROR -- " + str(team_url) +  " **")
    return None

  df.columns = ['Map', 'Expand', 'MAP_WIN_RATE', 'MAP_W', 'MAP_L', 'ATK_START', 'DEF_START', 
                      'ATK_ROUND_WIN_RATE', 'ATK_ROUND_W','ATK_ROUND_L', 
                      'DEF_ROUND_WIN_RATE', 'DEF_ROUND_W', 'DEF_ROUND_L', 'Agent Compositions']
  df.drop(['Expand','Agent Compositions'], axis=1, inplace=True)
  if (len(df.tail(1)['ATK_START']) == 1):
    df.drop(df.tail(1).index,inplace=True) ## Drop Icebox Row

  df['Map'].fillna(method='ffill',inplace=True)
  df['MAP_COUNT'] = [int(''.join(filter(str.isdigit, x))) for x in df['Map']]
  df['Map'] = [x.split()[0] for x in df['Map']]

  ## Get Stats by Map
  map_stats = df[df["MAP_W"].str.contains(r"^\d+$")]
  map_stats.reset_index(inplace=True, drop=True)
  for col in ['MAP_WIN_RATE', 'ATK_ROUND_WIN_RATE', 'DEF_ROUND_WIN_RATE']:
    map_stats[col] = [int(''.join(filter(str.isdigit, x))) for x in map_stats[col]]

  map_stats[list(map_stats.columns[1:])] = map_stats[list(map_stats.columns[1:])].apply(pd.to_numeric)

  map_stats['ATK_ROUND_COUNT'] = map_stats['ATK_ROUND_W'] + map_stats['ATK_ROUND_L']
  map_stats['DEF_ROUND_COUNT'] =  map_stats['DEF_ROUND_W'] + map_stats['DEF_ROUND_L']
  map_stats['ROUND_TOTAL_COUNT'] = map_stats['ATK_ROUND_COUNT'] + map_stats['DEF_ROUND_COUNT']
  map_stats['TEAM'] = (team_url.split('/')[-2]).upper()

  return map_stats