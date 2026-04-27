import os
import random
import urllib.parse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

raw_origins = os.getenv("AI_CORS_ORIGINS", "")
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

if not allowed_origins:
    allowed_origins = [
        "https://ai.houseofrevera.com",
    ]

app = FastAPI(title="House of Revera AI Engine", version="2.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class OutfitRequest(BaseModel):
    category: str
    color: str


class PriceRequest(BaseModel):
    category: str
    condition: str


def search_market_for_styles(style_list):
    prices = ["£15.00", "£22.50", "£35.00", "£40.00", "£18.50", "£25.00", "£12.00"]
    results = []

    for style in style_list:
        encoded_query = urllib.parse.quote_plus(style)

        ebay_url = f"https://www.ebay.co.uk/sch/i.html?_nkw={encoded_query}"
        depop_url = f"https://www.depop.com/search/?q={encoded_query}"
        vinted_url = f"https://www.vinted.co.uk/catalog?search_text={encoded_query}"

        platform_choice = random.choice(
            [
                {"name": "eBay", "url": ebay_url},
                {"name": "Depop", "url": depop_url},
                {"name": "Vinted", "url": vinted_url},
            ]
        )

        results.append(
            {
                "name": style,
                "platform": platform_choice["name"],
                "price": random.choice(prices),
                "image": f"https://placehold.co/150/2a2a2a/FFFFFF.png?text={urllib.parse.quote(style)}",
                "link": platform_choice["url"],
            }
        )

    return results


@app.get("/")
def home():
    return {"status": "AI Engine Running", "version": "2.0.1"}


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/recommend")
def recommend_outfit(item: OutfitRequest):
    user_item = item.category.lower()
    match_styles = []

    if "shirt" in user_item or "top" in user_item or "hoodie" in user_item or "sweat" in user_item:
        match_styles = [
            "Vintage Levi's 501",
            "Carhartt Double Knee",
            "Baggy Cargo Pants",
            "Dickies 874 Work Pants",
            "Pleated Chino Trousers",
        ]
        suggestion_text = "Pants & Trousers"
    elif "pant" in user_item or "jeans" in user_item or "trouser" in user_item or "short" in user_item:
        match_styles = [
            "Vintage Band Tee",
            "Oversized Hoodie",
            "Ralph Lauren Knit",
            "Flannel Check Shirt",
            "Nascar Racing Jacket",
        ]
        suggestion_text = "Tops & Layers"
    else:
        match_styles = [
            "Nike Air Jordan 1",
            "Vintage Tote Bag",
            "Silver Chain Necklace",
            "New Era Fitted Cap",
            "Denim Jacket",
        ]
        suggestion_text = "Accessories & Shoes"

    market_finds = search_market_for_styles(match_styles)

    return {
        "user_has": f"{item.color} {item.category}",
        "suggested_pairing": suggestion_text,
        "recommendations": market_finds,
    }


@app.post("/estimate")
def estimate_price(item: PriceRequest):
    category = item.category.lower()
    condition = item.condition.strip()

    if "shirt" in category:
        base_price = 20
    elif "jeans" in category:
        base_price = 35
    elif "jacket" in category:
        base_price = 50
    elif "shoe" in category:
        base_price = 60
    else:
        base_price = 15

    if condition == "New with tags":
        multiplier = 1.0
    elif condition == "Like New":
        multiplier = 0.8
    elif condition == "Good":
        multiplier = 0.6
    else:
        multiplier = 0.4

    estimated = round(base_price * multiplier, 2)

    return {
        "min": max(0, round(estimated - 5, 2)),
        "max": round(estimated + 5, 2),
        "suggested": estimated,
    }
