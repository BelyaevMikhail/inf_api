import scrapy
from scrapy.http import HtmlResponse
from parser.items import ParserItem


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://novosibirsk.hh.ru/search/vacancy?text=Python&from=suggest_post&area=4"]

    def parse(self, response:HtmlResponse, **kwargs):
        links = response.xpath("//a[@class='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):

        name = response.xpath("//h1/text()").get()
        url = response.url
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        yield ParserItem(name=name, url=url, salary=salary)
