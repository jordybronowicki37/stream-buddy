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
    def __init__(self, name: str, url: str, show_url: bool, selector: str, timeout: int, notify_when_online: bool, notify_when_offline: bool):
        self.name = name
        self.url = url
        self.show_url = show_url
        self.selector = selector
        self.timeout = timeout
        self.notify_when_online = notify_when_online
        self.notify_when_offline = notify_when_offline
        self.status = OnlineStatus.UNKNOWN

        self._just_live = False
        self._just_offline = False
        self._online_from: datetime | None = None
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

    def get_stream_log(self):
        if self.status == OnlineStatus.OFFLINE and self._online_from is not None and self._last_positive_live_check is not None:
            return {"start_time": self._online_from, "end_time": self._last_positive_live_check}
        return None

    def check_live(self, page: Page):
        # Checks if the user was seen online in the setup timeout time
        recently_online = self._last_positive_live_check is not None and datetime.now() - self._last_positive_live_check > timedelta(minutes=self.timeout)
        last_status = self.status
        was_offline = not self.is_live()
        is_live = False

        # Reset recent change values
        self._just_live = False
        self._just_offline = False

        # Check the live status in intervals
        page.goto(self.url)
        for _ in range(10):
            sleep(0.5)
            live_indicator = page.query_selector(self.selector)
            is_live = live_indicator is not None
            if is_live:
                break

        if is_live:
            self._last_positive_live_check = datetime.now()
            if was_offline:
                self._just_live = True
                self._online_from = datetime.now()
            self.status = OnlineStatus.ONLINE
        elif last_status == OnlineStatus.ONLINE:
            self.status = OnlineStatus.GRACE_PERIOD
        elif last_status == OnlineStatus.GRACE_PERIOD and not recently_online:
            self._just_offline = True
            self.status = OnlineStatus.OFFLINE
