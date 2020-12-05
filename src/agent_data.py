import pandas as pd 

## Web Scraping
import bs4
from bs4 import BeautifulSoup as soup
import urllib
from urllib.request import urlopen as uReq

AGENTS = ['omen', 'cypher', 'sova', 'jett', 'raze', 'breach', 'phoenix', 'reyna', 'killjoy' ,'sage' , 'brimstone', 'viper', 'Skye']

## Clean + Format numeric data on agent table
def CleanAgentPick(df):
  
  df['Map'] = ['Total'] + [str(x).split()[-1] for x in df['Map'][1:]]

  for col in df.columns[2:]:
    df[col] = [int(''.join(filter(str.isdigit, x))) for x in  df[col]]

  return df
  
## Retrieve Agents Picks Table from given event/tournment.
def EventAgentPick(event_url):

  try:
    df_agent_pick = pd.read_html(event_url)[0]
  except:
    print("** DATA FRAME READ ERROR **")

  agents_src = []
  agent_list = []

  # Agent name scraping (ordered by pick rate)
  try:
    client = uReq(event_url)
    page_html = client.read()
  except urllib.error.URLError as err:
    print("HTTP Error 404: " + str(event_url) + " Not Found")
    client.close()
  client.close()

  try:
    page_soup = soup(page_html,"html.parser")
    agents_table = page_soup.find("table",{"class": "wf-table mod-pr-global"})
    agents_src = agents_table.findAll("img")
  except:
    print("** NO INFO **")
    return None

  for src in agents_src:
    for x in AGENTS:
      if x in str(src):
        agent_list.append(x.upper())

  df_agent_pick.columns = ['MAP','NUM_MATCHES','ATK_WIN', 'DEF_WIN'] + agent_list

  df_agent_pick = CleanAgentPick(df_agent_pick)

  return df_agent_pick