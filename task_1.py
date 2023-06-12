from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re


client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_info']
vacancy_collection = db.vacancies


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '109.0.0.0 Safari/537.36'}
url = 'https://spb.hh.ru/search/vacancy'
vacancy_list = []
params = {'search_field': 'name', 'text': 'Python', 'page': 0}
session = requests.Session()
while True:
    response = session.get(url=url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancy = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})
    if len(vacancy) == 0:
        break
    params['page'] += 1
    for item in vacancy:
        vacancy_data = {}
        block_a = item.find('a', {'class': 'bloko-link'})
        href = block_a.get('href')
        name = block_a.text
        salary = item.find('span', {'class': 'bloko-header-section-3'})
        if salary:
            salary = salary.text
        vacancy_data['name'] = name
        vacancy_data['href'] = href
        vacancy_data['where_published'] = 'hh.ru'
        salary_data = {}
        salary_value = (str(salary)).replace('\u202f', '')
        if salary_value[0].isdigit():
            re_minimum_maximum = re.compile(r'\d+')
            re_currency = re.compile(r'\w+')
            minimum = re_minimum_maximum.findall(salary_value)[0]
            maximum = re_minimum_maximum.findall(salary_value)[1]
            currency = re_currency.findall(salary_value)[-1]
            salary_data['minimum'] = int(minimum)
            salary_data['maximum'] = int(maximum)
            salary_data['currency'] = currency
            vacancy_data['salary'] = salary_data
            print(vacancy_data)
        if salary_value[0] == 'о':
            re_minimum_maximum = re.compile(r'\d+')
            re_currency = re.compile(r'\w+')
            minimum = re_minimum_maximum.findall(salary_value)[0]
            currency = re_currency.findall(salary_value)[-1]
            salary_data['minimum'] = int(minimum)
            salary_data['currency'] = currency
            vacancy_data['salary'] = salary_data
        if salary_value[0] == 'д':
            re_minimum_maximum = re.compile(r'\d+')
            re_currency = re.compile(r'\w+')
            maximum = re_minimum_maximum.findall(salary_value)[0]
            currency = re_currency.findall(salary_value)[-1]
            salary_data['maximum'] = int(maximum)
            salary_data['currency'] = currency
            vacancy_data['salary'] = salary_data
        if salary_value == 'None':
            vacancy_data['salary'] = None
        if vacancy_collection.find_one({'href': vacancy_data['href']}):
            pass
        else:
            vacancy_collection.insert_one(vacancy_data)

print(len(list(vacancy_collection.find({}))))
for item in vacancy_collection.find({}):
    print(item)
