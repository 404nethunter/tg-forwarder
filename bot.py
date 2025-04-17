import snscrape.modules.twitter as sntwitter
import requests
import time

USERNAME = "toscagame"
TELEGRAM_TOKEN = "7694011148:AAGtSmt3YdVIGkW5o2EFDPZFZjJ8CLYQLGU"
CHAT_ID = "@vTservers"  # oder als Zahl: -1001234567890

def get_latest_tweet(username):
    for tweet in sntwitter.TwitterUserScraper(username).get_items():
        return tweet.id

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

latest_id = None

while True:
    try:
        tweet_id = get_latest_tweet(USERNAME)
        if tweet_id and tweet_id != latest_id:
            latest_id = tweet_id
            tweet_url = f"https://twitter.com/{USERNAME}/status/{tweet_id}"
            send_telegram_message(tweet_url)
            print("Gesendet:", tweet_url)
        time.sleep(60)  # alle 60 Sekunden checken
    except Exception as e:
        print("Fehler:", e)
        time.sleep(60)
