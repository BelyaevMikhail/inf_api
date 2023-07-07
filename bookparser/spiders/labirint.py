import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem
from scrapy.loader import ItemLoader

from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = "iabirint"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='product-title-link']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='cover']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response):
        print()
        loader = ItemLoader(item=BookparserItem(), response=response)
        loader.add_xpath('author_and_title', "//h1/text()").get()
        loader.add_xpath('price', "//span[@class='buying-pricenew-val-number']/text()").get()
        loader.add_xpath('publishing_house', "//a[@data-event-label='publisher']/text()").get()
        loader.add_xpath('rating', "//div[@id='rate']/text()").get()
        loader.add_xpath('photos', "//div[@id='product-image']/img/@data-src").get()

        loader.add_value('url', response.url)
        yield loader.load_item()
