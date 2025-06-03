from enum import Enum
from time import sleep
from datetime import datetime, timedelta

from playwright.sync_api import Page


class OnlineStatus(Enum):
    UNKNOWN = 0
    OFFLINE = 1
    GRACE_PERIOD = 2
    ONLINE = 3


class Streamer:
    def __init__(self, name, url, selector):
        self.name = name
        self.url = url
        self.selector = selector
        self.status = OnlineStatus.UNKNOWN
        self._just_live = False
        self._just_offline = False
        self._last_positive_live_check: datetime | None = None

    def is_live(self):
        return self.status == OnlineStatus.ONLINE or self.status == OnlineStatus.GRACE_PERIOD

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
        # Checks if the user was seen online in the past 5 minutes
        recently_online = self._last_positive_live_check is not None and datetime.now() - self._last_positive_live_check > timedelta(minutes=5)
        last_status = self.status
        was_offline = not self.is_live()
        is_live = False

        # Reset recent change values
        self._just_live = False
        self._just_offline = False

        # Check the live status in intervals
        page.goto(self.url)
        for i in range(20):
            sleep(0.5)
            live_indicator = page.query_selector(self.selector)
            is_live = live_indicator is not None
            if is_live:
                break

        if is_live:
            self._last_positive_live_check = datetime.now()
            if was_offline:
                self._just_live = True
            self.status = OnlineStatus.ONLINE
        elif last_status == OnlineStatus.ONLINE:
            self.status = OnlineStatus.GRACE_PERIOD
        elif last_status == OnlineStatus.GRACE_PERIOD and not recently_online:
            self._just_offline = True
            self.status = OnlineStatus.OFFLINE
