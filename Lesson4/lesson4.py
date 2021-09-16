# Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/93.0.4577.82 Safari/537.36'}

news = []

# https://mail.ru/
mail_url = 'https://news.mail.ru/inregions/siberian/54/society/'
response_mail = requests.get(mail_url, headers=header)
dom_mail = html.fromstring(response_mail.text)

source_mail = dom_mail.xpath('//*[@class="newsitem__param"]/text()')
title_mail = dom_mail.xpath('//*[@class="newsitem__title-inner"]/text()')
link_mail = dom_mail.xpath('//*[@class="newsitem__title link-holder"]/@href')
date_mail = dom_mail.xpath('//*[@class="newsitem__param js-ago"]/text()')

for i in range(3):
    data = {}
    data['source'] = source_mail[i]
    data['title'] = title_mail[i]
    data['link'] = mail_url[:-31] + link_mail[i]
    data['date'] = date_mail[i]
    news.append(data)

# https://yandex.ru/
yandex_url = 'https://yandex.ru/news/region/novosibirsk'
response_yandex = requests.get(yandex_url, headers=header)
dom_yandex = html.fromstring(response_yandex.text)

source_yandex = dom_yandex.xpath('//*[@class="mg-card__source-link"]/text()')
title_yandex = dom_yandex.xpath('//*[@class="mg-card__title"]/text()')
link_yandex = dom_yandex.xpath('//*[@class="mg-card__link"]/@href')
date_yandex = dom_yandex.xpath('//*[@class="mg-card-source__time"]/text()')

for i in range(3):
    data = {}
    data['source'] = source_yandex[i]
    data['title'] = title_yandex[i]
    data['link'] = link_yandex[i]
    data['date'] = date_yandex[i]
    news.append(data)

# https://lenta.ru/

lenta_url = 'https://lenta.ru/'
response_lenta = requests.get(lenta_url, headers=header)
dom_lenta = html.fromstring(response_lenta.text)

# source_yandex = dom_lenta.xpath('')
title_lenta = dom_lenta.xpath('//*[@id="root"]/section/div/div/div/section/div/div/a/text()') #.replace("\xa0",' ')
link_lenta = dom_lenta.xpath('//*[@id="root"]/section/div/div/div/section/div/div/a/@href')
date_lenta = dom_lenta.xpath('//*[@class="g-time"]/text()')

for i in range(3):
    data = {}
    data['source'] = lenta_url
    data['title'] = title_lenta[i]
    data['link'] = lenta_url + link_lenta[i]
    data['date'] = date_lenta[i]
    news.append(data)

client = MongoClient('localhost', 27017)
db = client['news']
news_collection = db.news
news_collection.insert_many(news)
