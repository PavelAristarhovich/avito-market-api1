from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re
import os
import json

app = FastAPI(title="Авито Рыночные Цены API")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "chrome-extension://*,http://localhost:*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_prices():
    try:
        with open("prices.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Ошибка загрузки prices.json:", e)
        return {"iphone 13": 45000}

MARKET_PRICES = load_prices()

def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r'[^\w\s]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

@app.get("/api/market-price")
def get_market_price(title: str):
    norm = normalize_title(title)
    for key, price in MARKET_PRICES.items():
        if key in norm:
            return {"market_price": price, "matched": key, "source": "database"}
    if any(w in norm for w in ['ipad', 'планшет']):
        return {"market_price": 40000, "matched": "generic tablet", "source": "heuristic"}
    if any(w in norm for w in ['кроссовки', 'кеды', 'adidas', 'nike', 'jordan', 'new balance']):
        return {"market_price": 8000, "matched": "generic sneakers", "source": "heuristic"}
    if 'часы' in norm or 'watch' in norm:
        if 'apple' in norm:
            return {"market_price": 35000, "matched": "apple watch", "source": "heuristic"}
        else:
            return {"market_price": 6000, "matched": "generic watch", "source": "heuristic"}
    if 'macbook' in norm or 'ноутбук' in norm:
        return {"market_price": 60000, "matched": "generic laptop", "source": "heuristic"}
    if 'playstation' in norm or 'xbox' in norm or 'nintendo' in norm:
        return {"market_price": 40000, "matched": "gaming console", "source": "heuristic"}
    if 'canon' in norm or 'nikon' in norm or 'sony' in norm or 'фотоаппарат' in norm:
        return {"market_price": 70000, "matched": "camera", "source": "heuristic"}
    if 'пуховик' in norm or 'куртка' in norm or 'ботинки' in norm:
        return {"market_price": 7500, "matched": "outerwear", "source": "heuristic"}
    return {"market_price": None, "matched": None, "source": "unknown"}

@app.get("/health")
def health():
    return {"status": "ok", "prices_count": len(MARKET_PRICES)}
