import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import os

# -----------------------------
# Discord Webhook
# -----------------------------
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


# -----------------------------
# Product Hunt (RSS)
# -----------------------------
def get_producthunt():
    url = "https://www.producthunt.com/feed"
    feed = feedparser.parse(url)
    launches = []

    for entry in feed.entries[:10]:
        launches.append({
            "source": "Product Hunt",
            "title": entry.title,
            "link": entry.link
        })
    return launches


# -----------------------------
# BetaList (HTML Scraping)
# -----------------------------
def get_betalist():
    url = "https://betalist.com/latest"
    try:
        html = requests.get(url, timeout=10).text
    except:
        return []

    soup = BeautifulSoup(html, "html.parser")
    launches = []

    items = soup.select(".startup")[:10]
    for item in items:
        title = item.select_one(".name").get_text(strip=True)
        link = "https://betalist.com" + item.select_one("a")["href"]

        launches.append({
            "source": "BetaList",
            "title": title,
            "link": link
        })
    return launches


# -----------------------------
# IndieHackers (HTML Scraping)
# -----------------------------
def get_indiehackers():
    url = "https://www.indiehackers.com/launches"
    try:
        html = requests.get(url, timeout=10).text
    except:
        return []

    soup = BeautifulSoup(html, "html.parser")
    launches = []

    items = soup.select("a.launch-card")[:10]
    for item in items:
        title = item.get_text(strip=True)
        link = "https://www.indiehackers.com" + item["href"]

        launches.append({
            "source": "IndieHackers",
            "title": title,
            "link": link
        })
    return launches


# -----------------------------
# HackerNews (Show HN RSS)
# -----------------------------
def get_hackernews():
    url = "https://hnrss.org/show"
    feed = feedparser.parse(url)
    launches = []

    for entry in feed.entries[:10]:
        launches.append({
            "source": "HackerNews Show HN",
            "title": entry.title,
            "link": entry.link
        })
    return launches


# -----------------------------
# ارسال به دیسکورد
# -----------------------------
def send_to_discord(items):
    if not WEBHOOK_URL:
        print("ERROR: No webhook URL found.")
        return

    if not items:
        content = "⚠️ امروز هیچ سایت جدیدی پیدا نشد."
    else:
        content = f"🔥 **New Website Launches — {datetime.now().strftime('%Y-%m-%d')}**\n\n"
        for item in items:
            content += f"**{item['source']}** — {item['title']}\n{item['link']}\n\n"

    data = {"content": content[:1800]}
    requests.post(WEBHOOK_URL, json=data)


# -----------------------------
# اجرای سیستم
# -----------------------------
def run():
    items = []
    items.extend(get_producthunt())
    items.extend(get_betalist())
    items.extend(get_indiehackers())
    items.extend(get_hackernews())

    send_to_discord(items)


if __name__ == "__main__":
    run()
