#!/usr/bin/python3

import pandas as pd 

from scraping.player_stats import PlayerStats
from scraping.match_economy_stats import MatchEconStats
from scraping.match_overview_stats import MatchOverviewStats
from scraping.match_performance_stats import MatchPerfStats
from scraping.team_stats import TeamMapStats


'''def PlayerStatsCSV(URL, out_file):
    
    data = [PlayerStats(URL)]'''

def TeamMapDataCSV(URL, out_filename):

    data = TeamMapStats(URL)
    out_filename = out_filename + '.csv'
    data.to_csv(out_filename, index=False)

def PlayerDataCSV(URLS, out_filename):

    data = [PlayerStats(url) for url in URLS]
    out = pd.concat([x for x in data], ignore_index=True) #df

    out_filename = out_filename + '.csv'

    out.to_csv(out_filename, index=False)

def EconomyDataCSV(URLS, out_filename):

    data = [MatchEconStats(url) for url in URLS]
    matches =  pd.concat([x[0] for x in data], ignore_index=True) #df
    maps = pd.concat([pd.concat(x[1], ignore_index=True)  for x in data], ignore_index=True) #df
    
    out_filename_match = out_filename + '_MATCHES.csv'
    out_filename_maps = out_filename + '_MAPS.csv'
    
    matches.to_csv(out_filename_match, index=False)
    maps.to_csv(out_filename_maps, index=False)
    
def OverviewDataCSV(URLS, out_filename):

    data = [MatchOverviewStats(url) for url in URLS]
    matches =  pd.concat([x[0] for x in data], ignore_index=True) #df
    maps = pd.concat([pd.concat(x[1:], ignore_index=True) for x in data], ignore_index=True) #df

    out_filename_match = out_filename + '_MATCHES.csv'
    out_filename_maps = out_filename + '_MAPS.csv'
    
    matches.to_csv(out_filename_match, index=False)
    maps.to_csv(out_filename_maps, index=False)

def PerformanceDataCSV(URLS, out_filename):

    data = [MatchPerfStats(url) for url in URLS]
    matches =  pd.concat([x[1] for x in data], ignore_index=True) #df
    maps = pd.concat([pd.concat(x[2],ignore_index=True) for x in data], ignore_index=True) #df

    out_filename_match = out_filename + '_MATCHES.csv'
    out_filename_maps = out_filename + '_MAPS.csv'
    
    matches.to_csv(out_filename_match, index=False)
    maps.to_csv(out_filename_maps, index=False)