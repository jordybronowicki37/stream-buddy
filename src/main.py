import threading

import sys
from os import getenv
import signal

import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page

from data_handler import DataHandler
from discord_notification import send_online_notification, send_offline_notification
from scheduling import extend_function_runtime
from logger import get_logger
from discord_bot import start_discord_bot
from streamer import Streamer, OnlineStatus

logger = get_logger('main')
streamers: list[Streamer] = []
data_handler = DataHandler()


def handle_sigterm(signum, frame):
    logger.info('Received signal to terminate.')
    for streamer in streamers:
        if streamer.status == OnlineStatus.OFFLINE:
            continue
        stream_log = streamer.get_stream_log()
        if stream_log is not None:
            data_handler.add_stream_log(streamer.name, stream_log.get("start_time"), stream_log.get("end_time"))
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_sigterm)


def load_environment():
    logger.info("Loading environment")
    load_dotenv()
    webhook_url = getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        logger.info("No webhook URL set")
        sys.exit(1)
    result = requests.get(webhook_url)
    if result.status_code != 200:
        logger.info("Webhook URL is not valid")
        sys.exit(1)


def check_streamers(page: Page, ls: list[Streamer]):
    for s in ls:
        s.check_live(page)
        if s.is_just_live():
            logger.info(f"Streamer {s.name} is live!")
            send_online_notification(s)
        elif s.is_just_offline():
            logger.info(f"Streamer {s.name} just went offline!")
            stream_log = s.get_stream_log()
            if stream_log is not None:
                data_handler.add_stream_log(s.name, stream_log.get("start_time"), stream_log.get("end_time"))
            send_offline_notification(s)


def start_browser():
    logger.info("Starting browser")
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Check loop
        logger.info("Starting application loop")
        while True:
            extend_function_runtime(60, lambda: check_streamers(page, streamers))
    except KeyboardInterrupt:
        logger.error("Interrupted. Cleaning up.")
    finally:
        browser.close()
        p.stop()


if __name__ == "__main__":
    load_environment()
    threading.Thread(target=start_browser).start()
    start_discord_bot()
