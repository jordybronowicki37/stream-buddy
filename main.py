import os

from dotenv import load_dotenv
from check_streamer import is_live
from discord_notification import send_online_notification

if __name__ == '__main__':
    load_dotenv()
    url = os.getenv("STREAM_URL")
    if is_live(url):
        print("Streamer is live!")
        send_online_notification(url.split("/")[-1])
    else:
        print("Streamer is offline.")
