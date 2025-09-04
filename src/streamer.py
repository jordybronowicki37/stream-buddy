from enum import Enum
from time import sleep
from datetime import datetime, timedelta

from playwright.sync_api import Page


class OnlineStatus(Enum):
    UNKNOWN = 0
    OFFLINE = 1
    GRACE_PERIOD_OFFLINE = 2
    GRACE_PERIOD_ONLINE = 3
    ONLINE = 4


class Streamer:
    def __init__(self, data_object: dict):
        self.name = data_object["name"]
        self.url = data_object["url"]
        self.show_url = data_object["show_url"]
        self.selector = data_object["selector"]
        self.online_grace_period = data_object["online_grace_period"]
        self.offline_grace_period = data_object["offline_grace_period"]
        self.notify_when_online = data_object["notify_when_online"]
        self.notify_when_offline = data_object["notify_when_offline"]
        self.status = OnlineStatus.UNKNOWN

        self._just_live = False
        self._just_offline = False
        self._online_from: datetime | None = None
        self._last_positive_live_check: datetime | None = None
        self._last_online_grace_period_check: datetime | None = None

    def is_live(self) -> bool:
        return self.status in [OnlineStatus.ONLINE, OnlineStatus.GRACE_PERIOD_OFFLINE]

    def is_just_live(self) -> bool:
        if self._just_live:
            self._just_live = False
            return True
        return False

    def is_just_offline(self) -> bool:
        if self._just_offline:
            self._just_offline = False
            return True
        return False

    def get_stream_log(self):
        if self.status == OnlineStatus.OFFLINE and self._online_from is not None and self._last_positive_live_check is not None:
            return {"start_time": self._online_from, "end_time": self._last_positive_live_check}
        return None

    def check_live(self, page: Page):
        # Checks if the user was seen online in the set offline grace period time
        recently_online = self._last_positive_live_check is not None and datetime.now() - self._last_positive_live_check > timedelta(minutes=self.offline_grace_period)
        last_status = self.status
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
            if last_status == OnlineStatus.OFFLINE:
                # Set online grace period check value if this is the first time seeing the streamer online
                if self._last_online_grace_period_check is None:
                    self._last_online_grace_period_check = datetime.now()

                is_past_online_grace_period = datetime.now() - self._last_online_grace_period_check > timedelta(minutes=self.online_grace_period)
                if is_past_online_grace_period:
                    self._just_live = True
                    self._online_from = self._last_online_grace_period_check
                    self.status = OnlineStatus.ONLINE
                    self._last_online_grace_period_check = None
            elif last_status == OnlineStatus.GRACE_PERIOD_OFFLINE:
                self.status = OnlineStatus.ONLINE
        elif last_status == OnlineStatus.ONLINE:
            self.status = OnlineStatus.GRACE_PERIOD_OFFLINE
        elif last_status == OnlineStatus.GRACE_PERIOD_OFFLINE and not recently_online:
            self._just_offline = True
            self.status = OnlineStatus.OFFLINE
