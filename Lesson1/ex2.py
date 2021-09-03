# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json
from pprint import pprint

print('Получите количество пролетающих ближе всего к Земле.')

start_date = input('Введите дату начала поиска астероидов в формате YYYY-MM-DD: ')
end_date = input('Введите дату конца поиска астероидов в формате YYYY-MM-DD, значение по умолчанию - неделя с даты начала: ')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
params = {'start-date': f"{start_date}",
          'end-date': f"{end_date}",
          "api_key": "MSjGdqW6r7e7wqB5a0G4T8geajWYCqzxn0vvq6i4"}
url = 'https://api.nasa.gov/neo/rest/v1/feed'

response = requests.get(url, params=params, headers=headers)

with open('lesson1.2.json', "w", encoding="utf-8") as file:
    file.write(response.text)

data = response.json()
print(
    f"С {start_date} до {end_date} максимально близко по своим траекториям к Земле пролетело {data['element_count']} метеоритов.")