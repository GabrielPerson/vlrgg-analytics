#!/usr/bin/python3

import pandas as pd
from pandas.core.common import SettingWithCopyWarning

## Retrieve players overall stats
## Read table from url
## Split Wins and Loses
## Convert number strings to numeric values
def PlayerStats(player_stats_url: str) -> pd.DataFrame():

  try:
    df = pd.read_html(player_stats_url)[0]
  except:
    print("** DATA FRAME READ ERROR -- " + str(player_stats_url) +  " **")
    return None

  df[['Team', 'CL_W', 'CL_T']] = None

  ## Create & Fill Teams Column
  df['Team'] = [x.split(' ')[-1]
                if len(x.split(' ')) > 1
                else ' '
                for x in df['Player']]
  
  df['Player'] = [ x.split(' ')[0] for x in df['Player'] ]
  
  df['CL%'] = [int(''.join(filter(str.isdigit, x)))
              if not pd.isna(x)
              else 0 
              for x in df['CL%']]

  df['HS%'] = [int(''.join(filter(str.isdigit, x))) 
              if not pd.isna(x)
              else None 
              for x in df['HS%']]

  df['CL_W'] = [int(x.split('/')[0]) 
                if not pd.isna(x) else None 
                for x in df['CL']]
  
  df['CL_T'] = [int(x.split('/')[1]) 
                if not pd.isna(x) else None 
                for x in df['CL']]  
  
  
  df.drop(['Agents', 'CL'], axis=1, inplace=True)

  ## Fix Mixwell team - ONLY MIXWELL BECAUSE HE IS CUTE
  #mixwell_index = df[df['Player'] == 'Mixwell'].index[0]
  #df.at[mixwell_index, 'Team'] = 'G2'

  return df