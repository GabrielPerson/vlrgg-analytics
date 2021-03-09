#!/usr/bin/python3

## Web Scraping
import bs4
from bs4 import BeautifulSoup as soup
import urllib
from urllib.request import urlopen as uReq

import pandas as pd 
import re
from pandas.core.common import SettingWithCopyWarning

MAPS = ['Haven', 'Bind', 'Split', 'Ascent', 'Icebox']

## Retrieve Match Map names
def GetMaps(page_html):

  try:
    page_soup = soup(page_html,"html.parser")
    div_maps = page_soup.find("div",{"class":"vm-stats-gamesnav-container"})
    map_src = div_maps.findAll("div", {"class":"vm-stats-gamesnav-item"})
  except:
    print("** NO INFO -- MAPS **")
    return None

  map_list = []
  map_adv = 0

  # MAPS BEST OF 1
  if len(map_src) == 0:
    map_str = page_soup.find("div",{"class":"map"}).text
    if map_str is None: return None
    else:
      for map_name in MAPS:
        if map_name in map_str: map_list.append(map_name.upper())
    return (map_list, map_adv)

  # MAPS BEST OF 3/4/5
  for src in map_src:
    for map_name in MAPS:
      if map_name in str(src):
        map_list.append(map_name.upper())
    if "Map Advantage" in str(src): map_adv = 1
  
  return (map_list, map_adv)

## Retrieve Agents used by each player on each match map
def GetAgents(page_html):

  agents = []

  try:
    page_soup = soup(page_html,"html.parser")
    div_stats = page_soup.find("div",{"class":"vm-stats-container"})
    mod_agents = div_stats.findAll("td",{"class":"mod-agents"})
  except:
    print("** NO INFO -- AGENTS **")
    return None
   
  #if mod_agents is not None:
  for x in mod_agents:
    img = x.find('img')
    if img is not None: agents.append(img.get('title'))
    else: agents.append('N/A')

  return agents

## Retrive rounds won by each team on each match map
def Scores(page_html):

  scores = []
  try:
    page_soup = soup(page_html,"html.parser")
    data_container = page_soup.find("div",{"class":"vm-stats-container"})
    all_scores = data_container.findAll("div",{"class":"score"})
  except:
    print("** NO INFO -- SCORES **")
    return None

  for tag in all_scores: scores.append(int(tag.text))

  return scores

## Retrieve rounds wonm by each team on each side (ATK/DEF)
def SideScores(page_html):

  scores_t = []
  scores_ct = []

  try:
    page_soup = soup(page_html,"html.parser")
    data_container = page_soup.find("div",{"class":"vm-stats-container"})
    all_ct = data_container.findAll("span",{"class":"mod-ct"})
    all_t = data_container.findAll("span",{"class":"mod-t"})
  except:
    print("** NO INFO -- SCORES **")
    return None

  for tag in all_ct: scores_ct.append(int(tag.text))
  for tag in all_t: scores_t.append(int(tag.text))

  return scores_t, scores_ct

## Get Valorant Patch Version of a match.
def GetPatchVer(page_html):

  regex = re.compile(r'\d.\d\d') 
  
  try:
    page_soup = soup(page_html,"html.parser")
    header_date = page_soup.find("div",{"class":"match-header-date"})
    patch = header_date.find("div", {"class":"wf-tooltip"}).text
  except:
    print("** NO INFO -- PATCH VERSION **")
    return None

  match = regex.search(patch)

  if match is not None: return float(match.group())
  else: return None