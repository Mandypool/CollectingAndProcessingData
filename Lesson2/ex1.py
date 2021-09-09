from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
import lxml
import json
import pandas as pd

dump = pd.DataFrame()

header = Headers(headers=True).generate()
url = 'https://rskrf.ru/ratings/produkty-pitaniya/'
prime_url = 'https://rskrf.ru'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

categories_names = [i.text for i in soup.find('div', class_='categories').find_all('span', class_='h5')]
categories_links = [i['href'] for i in soup.find('div', class_='categories').find_all('a', href=True)]

names_dict = {}
links_dict = {}
for i in range(len(categories_names)):
    response = requests.get(prime_url + categories_links[i])
    soup = BeautifulSoup(response.text, 'lxml')

    subcategories_names = [name.text for name in
                           soup.find('div', class_='categories').find_all('span', class_='d-xl-none d-block')]
    subcategories_links = [link['href'] for link in soup.find('div', class_='categories').find_all('a', href=True)]

    names_dict[categories_names[i]] = subcategories_names
    links_dict[categories_names[i]] = subcategories_links
    for j in range(len(names_dict[categories_names[i]])):
        response = requests.get(prime_url + links_dict[categories_names[i]][j])
        soup = BeautifulSoup(response.text, 'lxml')

        script = soup.find_all('script')[27].string.strip()[11:] + '}]}'
        end_index = script.index('$')
        script = script[:end_index - 3] + '}'

        data = json.loads(script)
        for k in range(len(data['items'])):
            try:
                points = [data['items'][k]['points']]
            except:
                points = 0

            try:
                quality = [data['items'][k]['indicator'][8]['value']]
            except:
                quality = 0

            try:
                secure = [data['items'][k]['indicator'][5]['value']]
            except:
                secure = 0

            try:
                name = [data['items'][k]['s_name']]
            except:
                name = 'None'

            temp_dump = pd.DataFrame({
                'Наименование': name,
                'Категория': [categories_names[i]],
                'Подкатегория': [names_dict[categories_names[i]][j]],
                'Безопасноcть': secure,
                'Качество': quality,
                'Общий балл': points,
                'URL': [prime_url + data['items'][k]['url']]
            })

            dump = dump.append(temp_dump, ignore_index=True)

pd.DataFrame(dump).to_csv('dump.csv', encoding='utf-8-sig')
