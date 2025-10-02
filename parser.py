import requests
from bs4 import BeautifulSoup
import time
import json
import random
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

QUERIES = [
    ("iphone 13", "phones"),
    ("ipad air", "tablets"),
    ("nike air force", "sneakers"),
    ("apple watch", "watches"),
    ("macbook air", "laptops"),
    ("диван угловой", "furniture"),
    ("велосипед горный", "bikes"),
    ("пуховик женский", "clothes"),
    ("playstation 5", "consoles"),
    ("canon eos", "cameras")
]

def scrape_avito(query, region="krasnodar", pages=2):
    prices = []
    for page in range(1, pages + 1):
        url = f"https://www.avito.ru/{region}?q={query}&p={page}"
        try:
            time.sleep(random.uniform(2, 4))
            res = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select('[itemprop="price"]')
            for item in items:
                price_str = item.get('content') or item.text
                price = re.sub(r'\D', '', price_str)
                if price and int(price) > 1000:
                    prices.append(int(price))
        except Exception as e:
            print(f"Ошибка при парсинге {query}: {e}")
    return prices

def update_prices():
    new_prices = {}
    try:
        with open("prices.json", "r", encoding="utf-8") as f:
            current = json.load(f)
    except:
        current = {}

    for query, _ in QUERIES:
        print(f"Парсинг: {query}")
        prices = scrape_avito(query)
        if prices:
            avg = int(sum(prices) / len(prices))
            new_prices[query] = avg
            print(f"  → Средняя цена: {avg} ₽ ({len(prices)} объявлений)")
        else:
            new_prices[query] = current.get(query, 30000)

    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(new_prices, f, ensure_ascii=False, indent=2)
    print("✅ База цен обновлена!")