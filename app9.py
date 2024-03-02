import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання посилання на наступну сторінку
def get_next_page_url(soup):
    next_button = soup.find('li', class_='next')
    if next_button:
        return next_button.find('a')['href']
    return None

# Список для зберігання цитат
quotes_data = []

# Список для зберігання інформації про авторів
authors_data = {}

# Посилання на початкову сторінку
url = 'http://quotes.toscrape.com/'

# Скрапінг
while url:
    # Запит на сайт
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Отримання цитат
    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author_name = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        quotes_data.append({'text': text, 'author': author_name, 'tags': tags})

        # Збереження інформації про авторів
        if author_name not in authors_data:
            authors_data[author_name] = {'name': author_name}

    # Отримання посилання на наступну сторінку
    url = get_next_page_url(soup)

# Збереження даних у JSON файли
with open('quotes.json', 'w') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

with open('authors.json', 'w') as f:
    json.dump(list(authors_data.values()), f, ensure_ascii=False, indent=4)

print("Скрапінг завершено.")