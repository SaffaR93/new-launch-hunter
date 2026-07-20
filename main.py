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

    for entry in feed.entries[:25]:  # فقط 25 لانچ جدید
        launches.append({
            "source": "Product Hunt",
            "title": entry.title,
            "link": entry.link
        })
    return launches

# -----------------------------
# 3) BetaList (RSS)
# -----------------------------
from bs4 import BeautifulSoup

def get_betalist():
    url = "https://betalist.com/latest"
    html = requests.get(url, timeout=10).text
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
# 4) IndieHackers (RSS)
# -----------------------------
def get_indiehackers():
    url = "https://www.indiehackers.com/launches"
    html = requests.get(url, timeout=10).text
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

# ------------------------------
# 5) HackerNews
#-------------------------------
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
