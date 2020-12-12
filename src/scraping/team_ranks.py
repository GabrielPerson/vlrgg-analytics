#!/usr/bin/python3
import pandas as pd
from pandas.core.common import SettingWithCopyWarning

## Get Team Rankings by Region
def TeamRankings(rank_url):
  
  try:
    df = pd.read_html(rank_url)[0]
  except:
    print("** DATA FRAME READ ERROR -- " + str(rank_url) +   " **")
    return None

  df.columns = ['Rank', 'Team', 'Rating', 'Last Played', 'Streak', 'Record', 'Winnings']

  df = CleanTeamRankings(df)

  return df

## Clean Team Rankings Data
def CleanTeamRankings(df):
  
  df[['Wins', 'Loses', 'Time_last_played_days', 'Last_opp']] = None

  ## Split Record
  df['Wins'] = [x.split('–')[0] for x in df['Record']]
  df['Loses'] = [x.split('–')[1] for x in df['Record']]

  ## Get Winning Numbers
  df['Winnings'] = [int(''.join(filter(str.isdigit, x))) for x in df['Winnings']]

  ## Last Played
  last_play = [x.split()[0] for x in df['Last Played']]
  df['Time_last_played_days'] = [int(''.join(filter(str.isdigit, x))) / 24 
                                    if x[-1] == 'h' 
                                    else int(''.join(filter(str.isdigit, x)))
                                    for x in last_play] 

  df['Last_opp'] = [' '.join(x.split()[3:]) for x in df['Last Played']]

  ## Streak to INT
  df['Streak'] = [int(''.join(filter(str.isdigit, x))) 
                    if x[-1] == 'W'
                    else int(''.join(filter(str.isdigit, x))) * -1
                    for x in df['Streak']]

  df.drop(['Record', 'Last Played'], axis=1, inplace=True)

  return df