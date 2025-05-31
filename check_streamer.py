from time import sleep

from playwright.sync_api import sync_playwright

def is_live(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        sleep(5)
        live_indicator = page.query_selector(".player-live-badge")
        browser.close()
        return live_indicator is not None
