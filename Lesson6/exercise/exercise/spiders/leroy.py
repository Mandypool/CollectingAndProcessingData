import scrapy
from scrapy.http import HtmlResponse
from ..items import ExerciseItem
from scrapy.loader import ItemLoader
import hashlib


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroySpider, self).__init__()
        self.name_base = search
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response, **kwargs):
        ads_links = response.xpath("//div[@class='phytpj4_plp largeCard']/a/@href").getall()
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        for link in ads_links:
            yield response.follow(f'https://leroymerlin.ru{link}', callback=self.ads_parse)

        if next_page:
            yield response.follow(f'https://leroymerlin.ru{next_page}', callback=self.parse)

    def ads_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=ExerciseItem(), response=response)
        loader.add_value('name_base', self.name_base)
        loader.add_value('_id', hashlib.sha1(str(response.url).encode()).hexdigest())
        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1[@slot="title"]/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('img', '//picture[@slot="pictures"]//img[@alt="product image"]/@src')
        parameters = response.xpath('//div[@class="def-list__group"]')
        parameter_list = dict()
        for param in parameters:
            parameter_list[param.xpath('.//dt[@class="def-list__term"]/text()').get()] \
                = param.xpath('.//dd[@class="def-list__definition"]/text()').get()
        loader.add_value('parameters', parameter_list)
        yield loader.load_item()
