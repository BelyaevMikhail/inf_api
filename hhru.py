import scrapy


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://novosibirsk.hh.ru/search/vacancy?text=Python&from=suggest_post&area=4"]

    def parse(self, response):
        pass
