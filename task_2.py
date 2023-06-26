from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_info']
vacancy = db.vacancy


def search(value):
    for item in vacancy.find({}):
        if item['salary'] is None:
            pass
        elif ['minimum', 'maximum', 'currency'] == list(item['salary'].keys()):
            if item['salary']['currency'] == 'руб':
                if item['salary']['minimum'] < value < item['salary']['maximum']:
                    print(item)
            if item['salary']['currency'] == 'USD':
                if item['salary']['minimum'] < value/72.8 < item['salary']['maximum']:
                    print(item)
            if item['salary']['currency'] == 'EUR':
                if item['salary']['minimum'] < value/78 < item['salary']['maximum']:
                    print(item)
            if item['salary']['currency'] == 'KZT':
                if item['salary']['minimum'] < value*6.2 < item['salary']['maximum']:
                    print(item)
        elif ['minimum', 'currency'] == list(item['salary'].keys()):
            if item['salary']['currency'] == 'руб':
                if item['salary']['minimum'] > value:
                    print(item)
            if item['salary']['currency'] == 'USD':
                if item['salary']['minimum'] > value / 72.8:
                    print(item)
            if item['salary']['currency'] == 'EUR':
                if item['salary']['minimum'] > value / 78:
                    print(item)
            if item['salary']['currency'] == 'KZT':
                if item['salary']['minimum'] > value * 6.2:
                    print(item)
        elif ['maximum', 'currency'] == list(item['salary'].keys()):
            if item['salary']['currency'] == 'руб':
                if value < item['salary']['maximum']:
                    print(item)
            if item['salary']['currency'] == 'USD':
                if value/72.8 < item['salary']['maximum']:
                    print(item)
            if item['salary']['currency'] == 'EUR':
                if value/78 < item['salary']['maximum']:
                    print(item)
            if item['salary']['currency'] == 'KZT':
                if value*6.2 < item['salary']['maximum']:
                    print(item)


search(100000)
