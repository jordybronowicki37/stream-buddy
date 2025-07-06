from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from discord_notification import send_online_notification, send_offline_notification
from scheduling import extend_function_runtime
from src.data_handler import get_streamers
from streamer import Streamer


def check_streamers(ls: list[Streamer]):
    for s in ls:
        s.check_live(page)
        if s.is_just_live():
            print(f"Streamer {s.name} is live!")
            send_online_notification(s)
        elif s.is_just_offline():
            print(f"Streamer {s.name} just went offline!")
            send_offline_notification(s)


if __name__ == '__main__':
    load_dotenv()

    # Read followed streamers data file
    streamers = get_streamers()

    # Start browser
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Check loop
        while True:
            extend_function_runtime(60, lambda: check_streamers(streamers))
    except KeyboardInterrupt:
        print("Interrupted. Cleaning up.")
    finally:
        browser.close()
        p.stop()
