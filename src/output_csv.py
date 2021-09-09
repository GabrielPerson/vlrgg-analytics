#!/usr/bin/python3

import pandas as pd 

from scraping.player_stats import PlayerStats
from scraping.match_economy_stats import MatchEconStats
from scraping.match_overview_stats import MatchOverviewStats
from scraping.match_performance_stats import MatchPerfStats
from scraping.team_stats import TeamMapStats


def TeamMapDataCSV(URLS: list, out_filename: str):

    data = [TeamMapStats(url) for url in URLS]
    out = pd.concat(data, ignore_index=True) #df

    out_filename = out_filename + '.csv'
    out.to_csv(out_filename, index=False)

def PlayerDataCSV(URLS: list, out_filename: str):

    data = [PlayerStats(url) for url in URLS]
    out = pd.concat(data, ignore_index=True) #df

    out.to_csv(out_filename + '.csv', index=False)

def EconomyDataCSV(URLS: list, out_filename: str):

    data = [MatchEconStats(url) for url in URLS]
    matches =  pd.concat([x[0] for x in data if x is not None], ignore_index=True) #df
    maps = pd.concat([pd.concat(x[1], ignore_index=True)  for x in data if x is not None], ignore_index=True) #df
    
    out_filename_match = out_filename + '_MATCHES.csv'
    out_filename_maps = out_filename + '_MAPS.csv'
    
    if matches is not None: matches.to_csv(out_filename_match, index=False)
    if maps is not None: maps.to_csv(out_filename_maps, index=False)
    
def OverviewDataCSV(URLS: list, out_filename: str):

    data= None
    matches= None 
    maps = None

    data = [MatchOverviewStats(url) for url in URLS]
    #data = Parallel(n_jobs=CORE_COUNT)(delayed(MatchOverviewStats)(url) for url in URLS)
    data = list(filter(None, data))
    if len(data) > 0:
        #matches =  pd.concat([x[0] for x in data if x is not None], ignore_index=True) #df
        maps = pd.concat([pd.concat(x[1:], ignore_index=True) for x in data if x is not None], ignore_index=True) #df

    out_filename_match = out_filename + '_MATCHES.csv'
    out_filename_maps = out_filename + '_MAPS.csv'
    
    if matches is not None: matches.to_csv(out_filename_match, index=False)
    if maps is not None: maps.to_csv(out_filename_maps, index=False)

def PerformanceDataCSV(URLS: list, out_filename: str):

    data= None
    matches= None 
    maps = None

    data = [MatchPerfStats(url) for url in URLS]
    matches =  pd.concat([x[1] for x in data if x is not None], ignore_index=True) #df
    maps = pd.concat([pd.concat(x[2],ignore_index=True) for x in data if x is not None], ignore_index=True) #df

    out_filename_match = out_filename + '_MATCHES.csv'
    out_filename_maps = out_filename + '_MAPS.csv'
    
    if matches is not None: matches.to_csv(out_filename_match, index=False)
    if maps is not None: maps.to_csv(out_filename_maps, index=False)