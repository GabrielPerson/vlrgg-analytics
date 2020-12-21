#!/usr/bin/python3
## Exporting
import pandas as pd 

from scraping.player_stats import PlayerStats
from scraping.match_economy_stats import MatchEconStats
from scraping.match_overview_stats import MatchOverviewStats
from scraping.match_performance_stats import MatchPerfStats
from scraping.team_stats import TeamMapStats
from pandas.core.common import SettingWithCopyWarning

## Write dataframes to Excel File
def DataFramesToExcel(df_list: list, file_name: str, sheet_names: list, show_index=False):
  
  writer = pd.ExcelWriter(file_name) # pylint: disable=abstract-class-instantiated
  for i, df in enumerate(df_list):
      df.to_excel(writer,sheet_name="{0}".format(sheet_names[i]),index=show_index)
  writer.save()

def TeamMapDataExcel(URLS: list, out_filename: str, sheets: list):

  data = [TeamMapStats(url) for url in URLS]
  DataFramesToExcel(data, out_filename, sheets)

def PlayerDataExcel(URLS: list, out_filename: str, sheets: list):
  
  data = [PlayerStats(url) for url in URLS]
  out =  [pd.concat(data, ignore_index=True)] #list of one df

  out_filename = out_filename + '.xlsx'

  DataFramesToExcel(out, out_filename, sheets)

def PerformanceDataExcel(URLS: list, out_filename: str, sheets: list):
  
  data = [MatchPerfStats(url) for url in URLS]
  #data_hxh = [x[0] for x in data] #list of dicts
  #data_hxh_all = [x['all_k'] for x in data_hxh]
  #data_hxh_first = [x['first_k'] for x in data_hxh] #list of dfs
  #data_hxh_op = [x['op_k'] for x in data_hxh] #list of dfs
  matches =  pd.concat([x[1] for x in data], ignore_index=True) #df
  maps = pd.concat([pd.concat(x[2],ignore_index=True) for x in data], ignore_index=True) #df
  out = [matches, maps]

  DataFramesToExcel(out, out_filename, sheets)

def EconomyDataExcel(URLS: list, out_filename: str, sheets: list):

  data = [MatchEconStats(url) for url in URLS]
  matches =  pd.concat([x[0] for x in data], ignore_index=True) #df
  maps = pd.concat([pd.concat(x[1], ignore_index=True)  for x in data], ignore_index=True) #df
  out = [matches, maps]

  DataFramesToExcel(out, out_filename, sheets)

def OverviewDataExcel(URLS: list, out_filename: str, sheets: list):

  data = [MatchOverviewStats(url) for url in URLS]
  matches =  pd.concat([x[0] for x in data], ignore_index=True) #df
  maps = pd.concat([pd.concat(x[1:], ignore_index=True) for x in data], ignore_index=True) #df
  out = [matches, maps]

  DataFramesToExcel(out , out_filename, sheets)