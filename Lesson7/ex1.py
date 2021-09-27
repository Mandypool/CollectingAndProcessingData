from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import hashlib
from random import getrandbits
from time import sleep

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
driver.get('https://mail.ru/')

wait = WebDriverWait(driver, 5)
name_wait = wait.until(EC.presence_of_element_located((By.NAME, 'login')))
login = driver.find_element_by_name('login')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.ENTER)
sleep(.5)

wait = WebDriverWait(driver, 5)
name_wait = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
password = driver.find_element_by_name('password')
password.send_keys('NextPassword172???')
password.send_keys(Keys.ENTER)

messages_link = set()

while True:
    flag = len(messages_link)
    try:
        wait = WebDriverWait(driver, 5)
        button_wait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dataset__items')))
    except:
        continue
    messages_block = driver.find_element_by_class_name('dataset__items')
    messages = messages_block.find_elements_by_tag_name('a')
    for message in messages:
        link = message.get_attribute('href')
        if (link is not None) and ('e.mail' in link):
            messages_link.add(link)
    if flag == len(messages_link): break

len(messages_link)

info_emails = []
for link in messages_link:
    info_email = {}
    driver.get(link)
    try:
        wait = WebDriverWait(driver, 5)
        button_wait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__date')))
        info_email['date'] = driver.find_element_by_class_name('letter__date').text
        info_email['name'] = driver.find_element_by_class_name('letter-contact').text
        info_email['name_email'] = driver.find_element_by_class_name('letter-contact').get_attribute('title')
        info_email['topic'] = driver.find_element_by_tag_name('h2').text
        info_email['text'] = driver.find_element_by_class_name('letter__body').text
        info_email['_id'] = hashlib.sha1(str(getrandbits(160)).encode()).hexdigest()
        info_emails.append(info_email)
    except:
        continue

client = MongoClient('localhost', 27017)
db = client['emails_db']
collections = db.messages
for item in info_emails:
    collections.update_one({'_id': {'$eq': item['_id']}}, {'$set': item}, upsert=True)

driver.close()
