from bs4 import BeautifulSoup as bs
import requests as req
import lxml
import pandas as pd
from fake_headers import Headers



url = 'https://roscontrol.com'
url1 = url + '/category/produkti/'
category = url + '/category/produkti/bakaleya/'
products = url + '/category/produkti/bakaleya/krupi-i-zlakovie-hlopya/'

res1 = req.get(url1)
soup = bs(res1.text, 'lxml')
cat_products = [i.text.strip() for i in soup.find_all(class_="catalog__category-name")]

res2 = req.get(url1 + category)
soup = bs(res2.text, 'lxml')
pod_cat_products = [i.text.strip() for i in soup.find_all(class_="catalog__category-name")]

res3 = req.get(url1 + products)
soup = bs(res3.text, 'lxml')
krupa = [i.text.strip() for i in soup.find_all(class_="product__item-link")]
links = [url + i['href'] for i in soup.find_all(class_='block-product-catalog__item')]

res_ocenki = []
for i in range(len(links)):
    res4 = req.get(links[i])
    soup = bs(res4.text, 'lxml')
    x = soup.find(id='product__single-rev-rating').text.split()
    res_ocenki.append(f'Общая = {x[0]}, Безопасность = {x[3]}, Качество = {x[10]}')

result = []
for num, i in enumerate(krupa):
    result.append({
        'Категория': cat_products[8],
        'Подкатегория': pod_cat_products[3],
        'Наименование': i,
        'Ссылка': links[num],
        'Оценка': res_ocenki[num]
    })

for i in result:
    print(i)

pd.DataFrame(result).to_csv('dump2.csv')