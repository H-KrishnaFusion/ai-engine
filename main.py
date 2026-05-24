import os
import urllib.parse
from decimal import Decimal, ROUND_HALF_UP

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

raw_origins = os.getenv("AI_CORS_ORIGINS", "")
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

if not allowed_origins:
    allowed_origins = [
        "https://ai.houseofrevera.com",
    ]

app = FastAPI(title="House of Revera AI Engine", version="2.2.1")

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


def normalize_text(value):
    return " ".join(str(value or "").strip().lower().split())


def title_text(value):
    return " ".join(word.capitalize() for word in normalize_text(value).split())


COLOR_FAMILIES = {
    "black": "neutral_dark",
    "charcoal": "neutral_dark",
    "grey": "neutral_mid",
    "gray": "neutral_mid",
    "white": "neutral_light",
    "cream": "neutral_light",
    "beige": "neutral_light",
    "tan": "earth",
    "camel": "earth",
    "brown": "earth",
    "olive": "earth",
    "khaki": "earth",
    "green": "earth",
    "blue": "cool",
    "navy": "cool",
    "denim": "cool",
    "red": "warm",
    "burgundy": "warm",
    "maroon": "warm",
    "pink": "soft",
    "blush": "soft",
    "lavender": "soft",
    "purple": "soft",
    "yellow": "bright",
    "mustard": "bright",
    "orange": "bright",
}


CATEGORY_KEYWORDS = {
    "tops": [
        "shirt",
        "top",
        "tee",
        "t-shirt",
        "tshirt",
        "blouse",
        "hoodie",
        "sweatshirt",
        "sweater",
        "jumper",
        "knit",
        "cardigan",
        "crop",
    ],
    "bottoms": [
        "pant",
        "pants",
        "jean",
        "jeans",
        "trouser",
        "trousers",
        "short",
        "shorts",
        "skirt",
        "leggings",
    ],
    "dresses": ["dress", "gown"],
    "outerwear": ["jacket", "coat", "blazer", "shacket", "outerwear"],
    "accessories": ["bag", "handbag", "purse", "belt"],
    "footwear": [
        "shoe",
        "shoes",
        "trainer",
        "trainers",
        "sneaker",
        "sneakers",
        "heel",
        "heels",
        "boot",
        "boots",
    ],
}


PAIRING_LIBRARY = {
    "tops": {
        "suggested_pairing": "Curated bottoms, bags and finishing pieces",
        "style_sets": {
            "neutral_dark": [
                "Stone wide-leg trousers",
                "Dark blue straight jeans",
                "Structured beige shoulder bag",
                "Minimal gold hoops",
                "Clean white trainers",
            ],
            "neutral_mid": [
                "White tailored trousers",
                "Black straight jeans",
                "Taupe crossbody bag",
                "Silver mini hoops",
                "Polished loafers",
            ],
            "neutral_light": [
                "Black tailored trousers",
                "Mid-wash relaxed denim",
                "Tan crossbody bag",
                "Delicate layered necklace",
                "Low-profile loafers",
            ],
            "earth": [
                "Ecru straight-leg jeans",
                "Chocolate tailored trousers",
                "Woven tan handbag",
                "Slim gold bracelet",
                "Soft suede flats",
            ],
            "cool": [
                "Off-white tailored trousers",
                "Charcoal pleated pants",
                "Silver-tone shoulder bag",
                "Fine silver hoops",
                "White leather sneakers",
            ],
            "warm": [
                "Cream wide-leg trousers",
                "Dark indigo denim",
                "Taupe mini bag",
                "Textured gold earrings",
                "Nude slingback heels",
            ],
            "soft": [
                "Soft grey straight trousers",
                "Light-wash denim",
                "Pearl-detail shoulder bag",
                "Rose-gold stud earrings",
                "Neutral ballet flats",
            ],
            "bright": [
                "White structured trousers",
                "Blue straight jeans",
                "Beige statement mini bag",
                "Polished gold hoops",
                "Clean platform trainers",
            ],
            "default": [
                "Black tailored trousers",
                "Classic blue denim",
                "Neutral crossbody bag",
                "Minimal hoop earrings",
                "Clean everyday sneakers",
            ],
        },
    },
    "bottoms": {
        "suggested_pairing": "Curated tops, layers and styling details",
        "style_sets": {
            "neutral_dark": [
                "Crisp white fitted top",
                "Soft beige knit cardigan",
                "Black cropped blazer",
                "Structured leather belt",
                "Pointed ankle boots",
            ],
            "neutral_mid": [
                "Black square-neck top",
                "White oversized shirt",
                "Charcoal fine-knit layer",
                "Slim leather belt",
                "Minimal loafers",
            ],
            "neutral_light": [
                "Black square-neck top",
                "Chocolate cropped knit",
                "Light trench layer",
                "Slim tan belt",
                "Minimal loafers",
            ],
            "earth": [
                "Ivory ribbed top",
                "Soft black cardigan",
                "Camel tailored blazer",
                "Gold buckle belt",
                "Cream low heels",
            ],
            "cool": [
                "White bodysuit",
                "Grey oversized blazer",
                "Navy fine-knit layer",
                "Silver buckle belt",
                "Clean white sneakers",
            ],
            "warm": [
                "Cream fitted blouse",
                "Black cropped jacket",
                "Soft taupe cardigan",
                "Slim gold belt",
                "Neutral kitten heels",
            ],
            "soft": [
                "White satin cami",
                "Light grey cardigan",
                "Muted beige blazer",
                "Delicate waist belt",
                "Soft-toned mules",
            ],
            "bright": [
                "Crisp white shirt",
                "Black fitted knit",
                "Neutral cropped blazer",
                "Polished belt",
                "Simple ankle boots",
            ],
            "default": [
                "Crisp white top",
                "Black fitted cardigan",
                "Neutral tailored blazer",
                "Classic slim belt",
                "Everyday loafers",
            ],
        },
    },
    "dresses": {
        "suggested_pairing": "Curated layers, bags and occasion-ready shoes",
        "style_sets": {
            "neutral_dark": [
                "Cream tailored blazer",
                "Black mini shoulder bag",
                "Gold statement earrings",
                "Nude strappy heels",
                "Light trench coat",
            ],
            "neutral_mid": [
                "Soft white blazer",
                "Silver clutch bag",
                "Crystal stud earrings",
                "Black pointed heels",
                "Longline coat",
            ],
            "neutral_light": [
                "Black cropped blazer",
                "Taupe top-handle bag",
                "Pearl earrings",
                "Soft beige heels",
                "Fine knit layer",
            ],
            "earth": [
                "Ivory cropped cardigan",
                "Tan structured handbag",
                "Gold cuff bracelet",
                "Cream slingback heels",
                "Camel wrap coat",
            ],
            "cool": [
                "Soft grey blazer",
                "Silver-tone clutch bag",
                "Crystal stud earrings",
                "White pointed heels",
                "Longline tailored coat",
            ],
            "warm": [
                "Champagne mini bag",
                "Textured gold earrings",
                "Cream block heels",
                "Neutral evening blazer",
                "Delicate bracelet stack",
            ],
            "soft": [
                "Pearl-detail cardigan",
                "Blush-toned clutch bag",
                "Rose-gold earrings",
                "Nude slingback heels",
                "Light tailored coat",
            ],
            "bright": [
                "White cropped blazer",
                "Neutral statement clutch",
                "Polished gold hoops",
                "Minimal heels",
                "Soft tailored layer",
            ],
            "default": [
                "Neutral tailored blazer",
                "Structured mini handbag",
                "Minimal statement earrings",
                "Elegant heels",
                "Light outer layer",
            ],
        },
    },
    "outerwear": {
        "suggested_pairing": "Curated core outfit pieces",
        "style_sets": {
            "neutral_dark": [
                "White fitted tee",
                "Blue straight jeans",
                "Fine grey knit",
                "Black leather shoulder bag",
                "Minimal ankle boots",
            ],
            "neutral_mid": [
                "Cream ribbed top",
                "Dark tailored trousers",
                "Fine black knit",
                "Structured shoulder bag",
                "Clean loafers",
            ],
            "neutral_light": [
                "Black fitted top",
                "Dark straight trousers",
                "Cream knit layer",
                "Tan crossbody bag",
                "Clean loafers",
            ],
            "earth": [
                "Ivory long-sleeve top",
                "Black tailored trousers",
                "Chocolate knit",
                "Woven tan bag",
                "Suede ankle boots",
            ],
            "cool": [
                "White ribbed top",
                "Charcoal trousers",
                "Blue denim base",
                "Silver-tone shoulder bag",
                "White trainers",
            ],
            "warm": [
                "Cream square-neck knit",
                "Dark blue denim",
                "Soft taupe top",
                "Gold-detail handbag",
                "Neutral boots",
            ],
            "soft": [
                "White bodysuit",
                "Grey straight-leg trousers",
                "Light knit top",
                "Pearl-detail bag",
                "Soft loafers",
            ],
            "bright": [
                "White clean-cut tee",
                "Dark tailored pants",
                "Neutral knit",
                "Structured mini bag",
                "Simple trainers",
            ],
            "default": [
                "White fitted top",
                "Straight-leg trousers",
                "Light knit layer",
                "Structured everyday bag",
                "Polished shoes",
            ],
        },
    },
    "accessories": {
        "suggested_pairing": "Curated outfits to style the accessory with",
        "style_sets": {
            "default": [
                "Cream blazer outfit",
                "Black tailored base",
                "Relaxed denim look",
                "Minimal gold jewellery",
                "Polished everyday loafers",
            ],
        },
    },
    "footwear": {
        "suggested_pairing": "Curated outfits to style the footwear with",
        "style_sets": {
            "default": [
                "Straight-leg denim outfit",
                "Clean white shirt",
                "Neutral blazer layer",
                "Minimal shoulder bag",
                "Simple everyday jewellery",
            ],
        },
    },
}


PRICE_RULES = {
    "coat": {"base": Decimal("25.00"), "spread": Decimal("0.00")},
    "jacket": {"base": Decimal("23.00"), "spread": Decimal("2.00")},
    "blazer": {"base": Decimal("22.00"), "spread": Decimal("2.00")},
    "dress": {"base": Decimal("19.00"), "spread": Decimal("3.00")},
    "jeans": {"base": Decimal("18.00"), "spread": Decimal("2.00")},
    "trouser": {"base": Decimal("17.00"), "spread": Decimal("2.00")},
    "trousers": {"base": Decimal("17.00"), "spread": Decimal("2.00")},
    "hoodie": {"base": Decimal("19.00"), "spread": Decimal("2.00")},
    "sweatshirt": {"base": Decimal("18.00"), "spread": Decimal("2.00")},
    "sweater": {"base": Decimal("18.00"), "spread": Decimal("2.00")},
    "jumper": {"base": Decimal("18.00"), "spread": Decimal("2.00")},
    "cardigan": {"base": Decimal("17.00"), "spread": Decimal("2.00")},
    "shirt": {"base": Decimal("14.00"), "spread": Decimal("2.00")},
    "blouse": {"base": Decimal("15.00"), "spread": Decimal("2.00")},
    "top": {"base": Decimal("13.00"), "spread": Decimal("2.00")},
    "skirt": {"base": Decimal("15.00"), "spread": Decimal("2.00")},
    "shorts": {"base": Decimal("12.00"), "spread": Decimal("2.00")},
    "short": {"base": Decimal("12.00"), "spread": Decimal("2.00")},
    "shoe": {"base": Decimal("23.00"), "spread": Decimal("1.00")},
    "shoes": {"base": Decimal("23.00"), "spread": Decimal("1.00")},
    "heels": {"base": Decimal("21.00"), "spread": Decimal("2.00")},
    "boots": {"base": Decimal("24.00"), "spread": Decimal("1.00")},
    "bag": {"base": Decimal("16.00"), "spread": Decimal("2.00")},
}


CONDITION_MULTIPLIERS = {
    "new with tags": Decimal("1.00"),
    "brand new": Decimal("0.98"),
    "like new": Decimal("0.92"),
    "excellent": Decimal("0.88"),
    "very good": Decimal("0.84"),
    "good": Decimal("0.78"),
    "fair": Decimal("0.66"),
    "well worn": Decimal("0.56"),
}


def round_money(value):
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def detect_group(category):
    category = normalize_text(category)

    for group, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in category for keyword in keywords):
            return group

    return "tops"


def detect_color_family(color):
    color = normalize_text(color)

    for known_color, family in COLOR_FAMILIES.items():
        if known_color in color:
            return family

    return "default"


def platform_for_index(index):
    platforms = ["Vinted", "Depop", "eBay", "Vinted", "Depop"]
    return platforms[index % len(platforms)]


def build_search_url(platform, style_name):
    encoded_query = urllib.parse.quote_plus(style_name)

    if platform == "eBay":
        return f"https://www.ebay.co.uk/sch/i.html?_nkw={encoded_query}"
    if platform == "Depop":
        return f"https://www.depop.com/search/?q={encoded_query}"

    return f"https://www.vinted.co.uk/catalog?search_text={encoded_query}"


def build_image_url(style_name):
    return f"https://placehold.co/300x400/F7F3EF/3A2E2A.png?text={urllib.parse.quote(style_name)}"


def unique_price_points(count):
    prices = [
        Decimal("9.00"),
        Decimal("12.00"),
        Decimal("15.00"),
        Decimal("19.00"),
        Decimal("23.00"),
    ]

    return prices[:count]


def search_market_for_styles(style_list):
    results = []
    prices = unique_price_points(len(style_list))

    for index, style in enumerate(style_list):
        platform = platform_for_index(index)

        result = {
            "name": style,
            "title": style,
            "platform": platform,
            "price": f"€{prices[index]:.2f}",
            "image": build_image_url(style),
            "image_url": build_image_url(style),
            "link": build_search_url(platform, style),
            "url": build_search_url(platform, style),
        }

        results.append(result)

    return results


def find_price_rule(category):
    category = normalize_text(category)

    for keyword, rule in PRICE_RULES.items():
        if keyword in category:
            return rule

    return {"base": Decimal("14.00"), "spread": Decimal("2.00")}


def condition_multiplier(condition):
    condition = normalize_text(condition)

    for key, multiplier in CONDITION_MULTIPLIERS.items():
        if key in condition:
            return multiplier

    return Decimal("0.74")


@app.get("/")
def home():
    return {"status": "AI Engine Running", "version": "2.2.1"}


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/recommend")
def recommend_outfit(item: OutfitRequest):
    group = detect_group(item.category)
    color_family = detect_color_family(item.color)

    style_config = PAIRING_LIBRARY[group]
    style_sets = style_config["style_sets"]
    match_styles = style_sets.get(color_family) or style_sets.get("default") or []

    user_has = f"{item.color} {item.category}".strip()
    pairing = style_config["suggested_pairing"]
    recommendations = search_market_for_styles(match_styles)

    return {
        # Existing response keys. Do not remove.
        "user_has": user_has,
        "suggested_pairing": pairing,
        "recommendations": recommendations,

        # Compatibility keys for frontend builds expecting these names.
        "pairing": pairing,
        "suggestedAdditions": recommendations,
        "items": recommendations,

        # Nested compatibility object for frontend builds expecting outfit.*
        "outfit": {
            "userHas": user_has,
            "user_has": user_has,
            "category": item.category,
            "color": item.color,
            "pairing": pairing,
            "suggested_pairing": pairing,
            "suggestedAdditions": recommendations,
            "items": recommendations,
            "recommendations": recommendations,
        },
    }


@app.post("/estimate")
def estimate_price(item: PriceRequest):
    rule = find_price_rule(item.category)
    multiplier = condition_multiplier(item.condition)

    suggested = rule["base"] * multiplier
    suggested = max(Decimal("5.00"), min(Decimal("25.00"), suggested))

    min_price = max(Decimal("5.00"), suggested - rule["spread"])
    max_price = min(Decimal("25.00"), suggested + rule["spread"])

    if min_price == max_price:
        if max_price < Decimal("25.00"):
            max_price += Decimal("1.00")
        else:
            min_price -= Decimal("1.00")

    return {
        "min": round_money(min_price),
        "max": round_money(max_price),
        "suggested": round_money(suggested),
    }
