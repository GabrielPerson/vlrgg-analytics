## Retrieve Match Map names
def GetMaps(url_match):

  try:
    client = uReq(url_match)
    page_html = client.read()
  except urllib.error.URLError as err:
    print("HTTP Error 404: " + str(event_url) + " Not Found")
    client.close()
  client.close()

  try:
    page_soup = soup(page_html,"html.parser")
    div_maps = page_soup.find("div",{"class":"vm-stats-gamesnav-container"})
    map_src = div_maps.findAll("div", {"class":"vm-stats-gamesnav-item"})
  except:
    print("** NO INFO **")
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
def GetAgents(url_match):

  agents = []

  try:
    client = uReq(url_match)
    page_html = client.read()
  except urllib.error.URLError as err:
    print("HTTP Error 404: " + str(url_match) + " Not Found")
    client.close()
  client.close()

  try:
    page_soup = soup(page_html,"html.parser")
    div_stats = page_soup.find("div",{"class":"vm-stats-container"})
    mod_agents = div_stats.findAll("td",{"class":"mod-agents"})
  except:
    print("** NO INFO **")
    return None
  
  #if mod_agents is not None:
  for x in mod_agents:
    img = x.find('img')
    if img is not None: agents.append(img.get('title'))
    else: agents.append('N/A')

  return agents

## Retrive rounds won by each team on each match map
def Scores(url_match):

  scores = []

  try:
    client = uReq(url_match)
    page_html = client.read()
  except urllib.error.URLError as err:
    return None
    client.close()
  client.close()

  try:
    page_soup = soup(page_html,"html.parser")
    data_container = page_soup.find("div",{"class":"vm-stats-container"})
    all_scores = data_container.findAll("div",{"class":"score"})
  except:
    print("** NO INFO **")
    return None

  for tag in all_scores: scores.append(int(tag.text))
  
  return score

## Get Valorant Patch Version of a match.
def GetPatchVer(url_match):

  regex = re.compile(r'\d.\d\d') 

  try:
    client = uReq(url_match)
    page_html = client.read()
  except urllib.error.URLError as err:
    print("HTTP Error 404: " + str(event_url) + " Not Found")
    client.close()
  client.close()

  try:
    page_soup = soup(page_html,"html.parser")
    header_date = page_soup.find("div",{"class":"match-header-date"})
    patch = header_date.find("div", {"class":"wf-tooltip"}).text
  except:
    print("** NO INFO **")
    return None

  match = regex.search(patch)

  return float(match.group())
