import requests
from lxml import html
from pprint import pprint

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
response = requests.get('https://lenta.ru/', headers=header)

dom = html.fromstring(response.text)

top_news = dom.xpath(".//h3[@class='card-big__title']/text()")
time_top = dom.xpath(".//time[@class='card-big__date']/text()")

super_top = ["Главная новость"]
first = top_news[:1]
time_first = time_top[:1]

pprint(super_top + first + time_first)

news_lenta = []

items = dom.xpath("//a[@class='card-mini _topnews']")
for item in items:
    lenta_news = {}
    source = item.xpath(".//a[@class='card-mini _topnews']/@href")
    news = item.xpath(".//span[@class='card-mini__title']/text()")
    news_time = item.xpath(".//time[@class='card-mini__date']/text()")

    lenta_news['Новость'] = news[:12]
    lenta_news['Время появленеия новости'] = news_time[:12]
    lenta_news['Источник'] = source[:12]

    news_lenta.append(lenta_news)

pprint(news_lenta)
