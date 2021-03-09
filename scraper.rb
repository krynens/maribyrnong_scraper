require 'scraperwiki'
require 'mechanize'

FileUtils.touch('data.sqlite')

today = Time.now.strftime('%Y-%m-%d')

url   = 'https://www.maribyrnong.vic.gov.au/Advertised-Planning-Applications'
agent = Mechanize.new
page  = agent.get(url)

table = page.search('article')
rows = table.search('a')

for row in rows do
  record = {}
  record['address'] = row.search('p.list-item-address').text.strip
  record['council_reference'] = row.search('p')[0].text.strip
  record['date_scraped'] = today
  record['description'] = row.search('p')[3].text.strip.sub(/caf\u00E9/, 'cafe')
  on_notice_to_raw = row.search('p')[2].text.strip.split('until ')[1].split(', ')[0]
  record['on_notice_to'] = DateTime.strptime(on_notice_to_raw, '%d %B %Y').strftime('%Y-%m-%d')
  record['info_url'] = row.to_s.split('"')[1]

  ScraperWiki.save_sqlite(['council_reference'], record)
end
