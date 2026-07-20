import requests
import feedparser
from datetime import datetime

# -----------------------------
# 1) Discord Webhook
# -----------------------------
WEBHOOK_URL = "https://discord.com/api/webhooks/1311548823209771091/G_VXKp2ym6NW_6IG_C0DpFBZOWAgKq94TqrPbGyekfky3fEAwBwvTtpBavDhntcJwtAu"

# -----------------------------
# 2) Product Hunt (RSS)
# -----------------------------
def get_producthunt():
    url = "https://www.producthunt.com/feed"
    feed = feedparser.parse(url)
    launches = []

    for entry in feed.entries[:25]:  # فقط ۱۰ لانچ جدید
        launches.append({
            "source": "Product Hunt",
            "title": entry.title,
            "link": entry.link
        })
    return launches

# -----------------------------
# 3) BetaList (RSS)
# -----------------------------
def get_betalist():
    url = "https://betalist.com/feed"
    feed = feedparser.parse(url)
    launches = []

    for entry in feed.entries[:10]:
        launches.append({
            "source": "BetaList",
            "title": entry.title,
            "link": entry.link
        })
    return launches

# -----------------------------
# 4) IndieHackers (RSS)
# -----------------------------
def get_indiehackers():
    url = "https://www.indiehackers.com/feed"
    feed = feedparser.parse(url)
    launches = []

    for entry in feed.entries[:10]:
        launches.append({
            "source": "IndieHackers",
            "title": entry.title,
            "link": entry.link
        })
    return launches

# -----------------------------
# 5) ارسال به دیسکورد
# -----------------------------
def send_to_discord(items):
    content = f"🔥 **New Website Launches — {datetime.now().strftime('%Y-%m-%d')}**\n\n"

    for item in items:
        content += f"**{item['source']}** — {item['title']}\n{item['link']}\n\n"

    data = {"content": content}
    requests.post(WEBHOOK_URL, json=data)

# -----------------------------
# 6) اجرای سیستم
# -----------------------------
def run():
    items = []
    items.extend(get_producthunt())
    items.extend(get_betalist())
    items.extend(get_indiehackers())

    send_to_discord(items)

run()
