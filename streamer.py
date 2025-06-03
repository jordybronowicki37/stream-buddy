from time import sleep
from datetime import datetime, timedelta

from playwright.sync_api import Page


class Streamer:
    def __init__(self, name, url, selector):
        self.name = name
        self.url = url
        self.selector = selector
        self._live = False
        self._just_live = False
        self._just_offline = False
        self._last_live_status = False
        self._last_positive_live_check: datetime | None = None

    def is_live(self):
        # Always return true if the last online check was less than 5 minutes ago
        if self._last_positive_live_check is not None and datetime.now() - self._last_positive_live_check > timedelta(minutes=5):
            self._last_live_status = True
            return True
        self._last_live_status = self._live
        return self._live

    def is_just_live(self):
        if self._just_live:
            self._just_live = False
            return True
        return False

    def is_just_offline(self):
        if self._just_offline:
            self._just_offline = False
            return True
        return False

    def check_live(self, page: Page):
        last_live_status = self._last_live_status
        was_offline = not self.is_live()
        is_live = False

        page.goto(self.url)
        sleep(1)
        for i in range(20):
            sleep(0.2)
            live_indicator = page.query_selector(self.selector)
            is_live = live_indicator is not None

            if is_live:
                self._last_positive_live_check = datetime.now()
                if was_offline:
                    self._just_live = True
                break

        if not is_live and last_live_status:
            self._just_offline = True

        self._live = is_live
