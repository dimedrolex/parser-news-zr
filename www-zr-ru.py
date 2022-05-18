import json
import requests
from bs4 import BeautifulSoup


URL = 'https://www.zr.ru/news/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0', 'accept': '*/*'}
HOST = 'https://www.zr.ru'


# Функция получения данных с сервера
def get_html(url, params=None):                                             # params - для определения числа страниц
    get_request = requests.get(url, headers=HEADERS, params=params)         # При помощи requests делается get-запрос к серверу 
    return get_request                                                      # Обьект r будет возвращён и использован в функции parse()


# Функция сбора данных с сайта
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='story-short')
    news = []
    for item in items[:10]:
        details = get_article_content(HOST + item.find('a', class_='link').get('href'))
        # Ограничился десятью постами, чтобы собрать больше статей требуется пагинация
        news.append({
            'title': item.find('a', class_='link').get_text(strip=True),
            'link': HOST + item.find('a', class_='link').get('href'),
            'article': item.find('div', class_='articles__item-desc').get_text(strip=True),
            'picture': HOST + item.find('img').get('src'),
            'autor': details['autor'],
            'date': details['date']
        })
    print(news)
    with open("db_zr.json", "w") as jfile:
        json.dump(news, jfile, indent=4, ensure_ascii=False)


# Функция сбора данных внутри статьи
def get_article_content(article_url):
    html = get_html(article_url)
    soup = BeautifulSoup(html.text, 'html.parser') 
    items = soup.find('body', class_='zr')
    return {
        'autor': items.find('span', class_='link_pink').get_text(strip=True),
        'date': items.find('div', class_='info__date').get_text(strip=True)
        }


# Основная функция парсинга первой страницы сайта
def parse():
    html = get_html(URL)
    # Проверяем связь со страицей
    if html.status_code == 200:        
        get_content(html.text)
    else:
        print('Error')   

parse()
