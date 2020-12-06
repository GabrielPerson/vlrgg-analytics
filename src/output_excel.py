#!/usr/bin/python3
## Exporting
import pandas as pd 

from match_economy_stats import MatchEconStats
from match_overview_stats import MatchOverviewStats
from match_performance_stats import MatchPerfStats
from team_stats import TeamMapStats
from pandas.core.common import SettingWithCopyWarning

## Write dataframes to Excel File
def DataFramesToExcel(df_list, file_name, sheet_names, show_index=False):
  
  writer = pd.ExcelWriter(file_name) # pylint: disable=abstract-class-instantiated
  for i, df in enumerate(df_list):
      df.to_excel(writer,sheet_name="{0}".format(sheet_names[i]),index=show_index)
  writer.save()

def TeamMapDataExcel(URLS, out_file, sheets):

  data = [TeamMapStats(url) for url in URLS]
  DataFramesToExcel(data, out_file, sheets)

def PerformanceDataExcel(URLS, out_file, sheets):
  
  data = [MatchPerfStats(url) for url in URLS]
  #data_hxh = [x[0] for x in data] #list of dicts
  #data_hxh_all = [x['all_k'] for x in data_hxh]
  #data_hxh_first = [x['first_k'] for x in data_hxh] #list of dfs
  #data_hxh_op = [x['op_k'] for x in data_hxh] #list of dfs
  matches =  pd.concat([x[1] for x in data], ignore_index=True) #df
  maps = pd.concat([pd.concat(x[2],ignore_index=True) for x in data], ignore_index=True) #df
  out = [matches, maps]

  DataFramesToExcel(out, out_file, sheets)

def EconomyDataExcel(URLS, out_file, sheets):

  data = [MatchEconStats(url) for url in URLS]
  matches =  pd.concat([x[0] for x in data], ignore_index=True) #df
  maps = pd.concat([pd.concat(x[1], ignore_index=True)  for x in data], ignore_index=True) #df
  out = [matches, maps]

  DataFramesToExcel(out, out_file, sheets)

def OverviewDataExcel(URLS, out_file, sheets):

  data = [MatchOverviewStats(url) for url in URLS]
  matches =  pd.concat([x[0] for x in data], ignore_index=True) #df
  maps = pd.concat([pd.concat(x[1:], ignore_index=True) for x in data], ignore_index=True) #df
  out = [matches, maps]

  DataFramesToExcel(out , out_file, sheets)