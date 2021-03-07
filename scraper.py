import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import scraperwiki

today = datetime.today()

url = 'https://www.maribyrnong.vic.gov.au/Advertised-Planning-Applications'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')

table = soup.find('div', class_='list-container da-list-container left')
rows = table.find_all('article')

for row in rows:
    record = {}
    record['address'] = row.find('p', class_='list-item-address').text.strip()
    record['date_scraped'] = today.strftime("%Y-%m-%d")
    record['description'] = row.find_all('p')[3].text.strip()
    record['council_reference'] = row.find(
        'p', class_='da-application-number small-text').text.strip()
    record['info_url'] = str(row.find('a')).split('"')[1]
    on_notice_to_raw = row.find(
        'p', class_='applications-closing display-until small-text display-until-date').text.strip().split('until ')[1].split(', ')[0]
    record['on_notice_to'] = datetime.strptime(on_notice_to_raw, '%d %B %Y').strftime("%Y-%m-%d")

    scraperwiki.sqlite.save(
        unique_keys=['council_reference'], data=record, table_name="data")
