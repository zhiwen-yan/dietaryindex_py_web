"""Pure-Python FII database helpers for API usage."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "fii_food_usda.csv"

FOOD_GROUP_RULES = [
    ("Supplements & Powders", ("powder", "herbalife", "supplement", "nutritional mix", "protein mix")),
    ("Mixed / Prepared Foods", ("pizza", "sandwich", "burger", "burrito", "taco", "lasagna", "fried rice", "soup", "stew", "casserole")),
    ("Oils & Fats", ("oil", "butter", "margarine", "shortening", "lard", "mayonnaise")),
    ("Beverages", ("tea", "coffee", "juice", "soda", "cola", "drink", "beverage", "water", "smoothie", "shake")),
    ("Sweets & Desserts", ("cake", "cookie", "pie", "pudding", "ice cream", "candy", "chocolate", "brownie", "donut", "doughnut", "fritter", "tart")),
    ("Grains & Bakery", ("bread", "rice", "pasta", "noodle", "cereal", "oat", "oatmeal", "cracker", "biscuit", "tortilla", "bagel", "bun", "muffin", "waffle", "pancake")),
    ("Dairy & Eggs", ("milk", "yogurt", "yoghurt", "cheese", "cream", "custard", "kefir", "egg")),
    ("Meat & Seafood", ("beef", "pork", "ham", "bacon", "sausage", "chicken", "turkey", "duck", "fish", "salmon", "tuna", "shrimp", "crab", "lobster", "octopus", "liver", "organ")),
    ("Legumes, Nuts & Soy", ("bean", "beans", "lentil", "chickpea", "pea", "peas", "peanut", "nut", "nuts", "soy", "tofu", "edamame", "tempeh", "seed", "seeds")),
    ("Vegetables", ("broccoli", "spinach", "lettuce", "carrot", "pepper", "cabbage", "kale", "celery", "cucumber", "onion", "garlic", "potato", "tomato", "asparagus", "mushroom", "parsley", "vegetable")),
    ("Fruits", ("apple", "banana", "orange", "berry", "berries", "grape", "melon", "pear", "peach", "plum", "pineapple", "mango", "papaya", "kiwi", "lemon", "lime", "tangerine", "avocado", "fig", "date", "raisin", "cranberry", "strawberry", "blueberry", "fruit")),
    ("Condiments & Seasonings", ("sauce", "seasoning", "spice", "vinegar", "mustard", "ketchup", "salsa", "dressing", "paste", "broth")),
]

def _normalize(value: object) -> str:
    text = str(value or "").lower().strip()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _classify_food_group(description: object) -> str:
    text = _normalize(description)
    for group, keywords in FOOD_GROUP_RULES:
        if any(keyword in text for keyword in keywords):
            return group
    return "Other / Uncategorized"


@lru_cache(maxsize=1)
def _load_db() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["FDCD"] = pd.to_numeric(df["FDCD"], errors="coerce").astype("Int64")
    df["FII"] = pd.to_numeric(df["FII"], errors="coerce")
    df["FII_score"] = pd.to_numeric(df["FII_score"], errors="coerce")
    df["Main_food_description"] = df["Main_food_description"].fillna("Unknown food")
    df = df.dropna(subset=["FDCD", "FII"]).copy()
    df["search_text"] = df["Main_food_description"].map(_normalize)
    df["food_group"] = df["Main_food_description"].map(_classify_food_group)
    df["direction"] = np.where(df["FII"] < 0, "anti", np.where(df["FII"] > 0, "pro", "neutral"))
    return df.reset_index(drop=True)


def get_fii_summary() -> dict:
    df = _load_db()
    return {
        "foods": int(len(df)),
        "groups": int(df["food_group"].nunique()),
        "group_names": sorted(df["food_group"].unique().tolist()),
        "anti": int((df["direction"] == "anti").sum()),
        "pro": int((df["direction"] == "pro").sum()),
    }


def search_fii(
    query: str = "",
    limit: int = 20,
    *,
    group: str | None = None,
    direction: str = "all",
    sort_by: str = "best_match",
) -> list[dict]:
    df = _load_db()
    term = _normalize(query)
    working = df
    if group:
        working = working[working["food_group"] == group]
    if direction in {"anti", "pro", "neutral"}:
        working = working[working["direction"] == direction]

    fdcd_text = working["FDCD"].astype(str)
    if term.isdigit():
        result = working[fdcd_text == term].head(limit)
        return [_serialize_row(row) for _, row in result.iterrows()]

    # The bundled USDA/FNDDS descriptions are English-only. Do not imply that
    # a few hard-coded translations constitute Chinese-language search.
    if term and not re.search(r"[a-z]", term):
        return []

    scores = pd.Series(0.0, index=working.index)
    if term:
        desc = working["search_text"]
        escaped = re.escape(term)
        pattern = re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", re.I)
        scores += np.where(desc == term, 120.0, 0.0)
        scores += np.where(desc.str.startswith(term, na=False), 45.0, 0.0)
        scores += np.where(desc.str.contains(pattern, na=False), 25.0, 0.0)
        scores += np.where(desc.str.contains(escaped, regex=True, na=False), 8.0, 0.0)
        result = working[scores > 0].copy()
    else:
        result = working.copy()
    if result.empty:
        return []

    result["_score"] = scores.loc[result.index]
    if sort_by == "fii_asc":
        result = result.sort_values(["FII", "Main_food_description"], ascending=[True, True])
    elif sort_by == "fii_desc":
        result = result.sort_values(["FII", "Main_food_description"], ascending=[False, True])
    elif sort_by == "score_desc":
        result = result.sort_values(["FII_score", "FII"], ascending=[False, True])
    elif sort_by == "az":
        result = result.sort_values("Main_food_description")
    elif term:
        result = result.sort_values(["_score", "FII", "Main_food_description"], ascending=[False, True, True])
    else:
        result = result.sort_values(["FII", "Main_food_description"], ascending=[True, True])
    result = result.head(limit)
    return [_serialize_row(row) for _, row in result.iterrows()]


def _serialize_row(row: pd.Series) -> dict:
    return {
        "fdcd": int(row["FDCD"]),
        "food": row["Main_food_description"],
        "fii": float(row["FII"]),
        "fii_score": float(row["FII_score"]) if not pd.isna(row["FII_score"]) else None,
        "food_group": row["food_group"],
        "source": "USDA-FCT",
        "direction": row["direction"],
    }


def get_fii_detail(fdcd: int) -> dict | None:
    df = _load_db()
    result = df[df["FDCD"] == fdcd]
    if result.empty:
        return None
    row = result.iloc[0]
    return _serialize_row(row)


def get_fii_peers(fdcd: int, limit: int = 5) -> dict | None:
    df = _load_db()
    selected = df[df["FDCD"] == fdcd]
    if selected.empty:
        return None
    group = selected.iloc[0]["food_group"]
    peers = df[(df["food_group"] == group) & (df["FDCD"] != fdcd)]
    anti = peers.sort_values(["FII", "Main_food_description"], ascending=[True, True]).head(limit)
    pro = peers.sort_values(["FII", "Main_food_description"], ascending=[False, True]).head(limit)
    return {
        "food_group": group,
        "anti": [_serialize_row(row) for _, row in anti.iterrows()],
        "pro": [_serialize_row(row) for _, row in pro.iterrows()],
    }
