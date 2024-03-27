from bs4 import BeautifulSoup
import requests
import re
import time

def scraper(url):
    page = requests.get(url)
    return page.text

def extract_match_info(url, id):
    def has_exact_classes(tag):
        return tag.name == 'div' and sorted(tag.get('class', [])) == ['cb-col', 'cb-col-73', 'cb-mat-fct-itm']

    pattern = r"/(\w+)-vs-(\w+)-"
    reg = re.search(pattern, url)
    team1 = reg.group(1)
    team2 = reg.group(2)

    match_info = {team1:[], team2:[]}

    html = scraper(url)
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all(has_exact_classes)

    for i in range(len(data)):
        if len(data[i].find_all()) == 11:
            players1 = data[i].find_all(class_='text-hvr-underline')
            for player in players1:
                match_info[team1].append(player.text.replace(' (wk)', '').replace(' (c)', '').replace(' (c & wk)', ''))

            players2 = data[i+3].find_all(class_='text-hvr-underline')
            for player in players2:
                match_info[team2].append(player.text.replace(' (wk)', '').replace(' (c)', '').replace(' (c & wk)', ''))
            break
    
    print(f'match {id} - {team1} vs {team2} done')
    return match_info

def parser():
    html = scraper('https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023/matches')

    soup = BeautifulSoup(html, 'html.parser')
    matches = soup.find_all(class_='text-hvr-underline')
    site = 'https://www.cricbuzz.com'

    match_urls= []
    for match in matches:
        if 'cricket-scores' in match.get('href'):
            match_urls.append(match.get('href').replace('cricket-scores', 'cricket-match-facts'))

    match_data, id = [], 1
    for url in match_urls:
        match_data.append(extract_match_info(f'{site}{url}', id))
        id += 1
        time.sleep(2)

    return match_data

match_data = parser()
print(match_data)