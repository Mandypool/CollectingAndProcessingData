# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient

main_link = 'https://hh.ru'

area = {
    'россия': [113, 'russia.'],
    'москва': [1, ''],
    'санкт-петербург': [2, 'spb.'],
    'новосибирск': [4, 'novosibirsk.'],
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.63 Safari/537.36'}

client = MongoClient('127.0.0.1', 27017)
db = client['job_db_1']

while True:
    city = input('Город поиска: ').lower()
    if city in area.keys():
        break
    else:
        print('нет таког города')
        print()
        print(f'Введите один из списка {area.keys()}')
vacancy = input('Вакансия: ')

params = {'clusters': 'true',
          'enable_snippets': 'true',
          'text': vacancy,
          'L_save_area': 'true',
          'area': {area[city][0]},
          'from': 'cluster_area',
          'showClusters': 'true'
          }


def salary(salary_str):
    min_max_c = [None, None, None]
    if salary_str == 'По договорённости':
        return min_max_c
    if salary_str:
        tmp = salary_str.replace('\xa0', ' ')
        k = 0
        tmp1 = list(tmp)
        diap = [x for x in range(48, 56)]
        for s in tmp[1:-2]:
            k += 1
            if (s == ' ') and (ord(tmp[k - 1]) in diap) and (ord(tmp[k + 1]) in diap):
                tmp1[k] = '!'
                tmp = ''.join(tmp1)
        tmp = tmp.replace('!', '')
        if salary_str[0] == 'о':
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = None
            min_max_c[0] = float(tmp.split()[1])
        elif salary_str[0] == 'д':
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = float(tmp.split()[1])
            min_max_c[0] = None
        elif salary_str.find('-') > -1:
            tmp = tmp.split('-')
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = float(tmp[1].split()[0])
            min_max_c[0] = float(tmp[0])
        else:
            min_max_c[2] = salary_str.split()[-1]
            min_max_c[1] = float(tmp.split()[0])
            min_max_c[0] = float(tmp.split()[0])
    return min_max_c


def salary_higher_than(salary_nuber):
    result = db.job.find({'$or': [{"salary_min": {'$gt': salary_nuber}}, {"salary_max": {'$gt': salary_nuber}}]},
                         {'_id': 0})
    print('\nСписок вакансий:')
    index = 0
    for i in result:
        pprint(i)
        index += 1
    print(f'Всего найденно вакансий: {index}')


def db_updata(DF_list):
    db.job.delete_many({})  # Del
    db.job.insert_many(DF_list)  # Upt


html = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
soup = bs(html.text, 'html.parser')
vacancies_block = soup.find('div', {'class': 'sticky-container'})
vacancies_list2 = vacancies_block.find_all('div', {'class': 'vacancy-serp-item__row'})

DataFrame_list = []

ii = 0
while True:
    soup = bs(html.text, 'html.parser')
    vacancies_block = soup.find('div', {'class': 'sticky-container'})
    vacancies_list2 = vacancies_block.find_all('div', {'class': 'vacancy-serp-item__row'})

    for i in vacancies_list2:
        vacancies_list3 = i.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        DataFrame_job = {}
        if vacancies_list3:
            ii += 1
            DataFrame_job['id'] = ii
            DataFrame_job['name'] = vacancies_list3.get_text()
            DataFrame_job['href'] = vacancies_list3.get('href')
            DataFrame_job['site'] = 'hh.ru'

            vacancies_list4 = i.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if vacancies_list4:
                mas = salary(vacancies_list4.get_text())
            else:
                mas = [None, None, None]
            DataFrame_job['salary_min'] = mas[0]
            DataFrame_job['salary_max'] = mas[1]
            DataFrame_job['salary_currency'] = mas[2]
            DataFrame_list.append(DataFrame_job)

    vv = vacancies_block.find('a', {'data-qa': 'pager-next'})
    print(vv)
    try:
        vv.get('href')
    except AttributeError:
        break
    else:
        html = requests.get(main_link + vv.get('href'), params=params, headers=headers)

print()
pprint(DataFrame_list)
db.job.insert_many(DataFrame_list)  # One time!

db_updata(DataFrame_list)

salary_search = None
while not salary_search:
    try:
        salary_search = int(input('Введите минимальную желаемую зарплату: '))
    except:
        print('Это не число')
        salary_search = None

salary_higher_than(salary_search)
