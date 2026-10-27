import requests
import csv
import os
from datetime import datetime, timezone, timedelta

PRODUCTS = [
    {
        "name": "藝聲 YESUNG FANSIGN",
        "route": "46756ad6feef74d93",
    },
]

BASE = "https://allmyday.com.tw/api/product/item/"
CSV_PATH = "allmyday_yesung.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/26.6.1 Safari/605.1.15",
    "Accept": "application/json",
}

def fetch(route):
    url = BASE + route
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()

def parse(name, data):
    tw = timezone(timedelta(hours=8))
    now = datetime.now(tw).strftime("%Y-%m-%d %H:%M:%S")
    p = data.get("data", {}).get("prod", {})
    if not p:
        return None
    return {
        "time": now,
        "name": name,
        "title": p.get("title", ""),
        "sales_amount": p.get("sales_amount", 0),
        "quantity": p.get("quantity", 0),
        "show_sales_amount": p.get("show_sales_amount", 0),
        "pre_order": p.get("pre_order", 0),
        "delisting_at": p.get("delisting_at", ""),
    }

def main():
    rows = []
    for item in PRODUCTS:
        try:
            data = fetch(item["route"])
            row = parse(item["name"], data)
            if row:
                rows.append(row)
                print(row)
        except Exception as e:
            print(f"[ERROR] {item['name']}: {e}")

    if not rows:
        print("沒有資料，結束")
        return

    new_file = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        if new_file:
            w.writeheader()
        w.writerows(rows)

if __name__ == "__main__":
    main()
