from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from ..exercise import settings
from spiders.leroy import LeroySpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroySpider, search='Гвозди')

    process.start()
