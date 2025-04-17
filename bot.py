import snscrape.modules.twitter as sntwitter
import requests
import json
import os
import time

# Einstellungen
USERNAME = "toscagame"
TELEGRAM_TOKEN = "7694011148:AAGtSmt3YdVIGkW5o2EFDPZFZjJ8CLYQLGU"
CHAT_ID = "@vTservers"  # oder deine Telegram-ID (z. B. 123456789)
STORAGE_FILE = "vtservers.json"

# Letzten Tweet laden
def load_last_tweet_id():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_id")
    return None


def save_last_tweet_id(tweet_id):
    with open(STORAGE_FILE, "w") as f:
        json.dump({"last_id": tweet_id}, f)


def get_latest_tweet(username):
    for tweet in sntwitter.TwitterUserScraper(username).get_items():
        return tweet.id
    return None


def send_to_telegram(tweet_id):
    tweet_url = f"https://x.com/{USERNAME}/status/{tweet_id}"
    message = f"Neuer Tweet von @{USERNAME}:\n{tweet_url}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

# Hauptlogik
def check_and_send():
    latest_id = get_latest_tweet(USERNAME)
    last_sent_id = load_last_tweet_id()

    if latest_id and latest_id != last_sent_id:
        send_to_telegram(latest_id)
        save_last_tweet_id(latest_id)
        print("Neuer Tweet gesendet!")
    else:
        print("Kein neuer Tweet.")

if __name__ == "__main__":
    check_and_send()
