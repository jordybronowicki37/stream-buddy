import json
from datetime import datetime
from pathlib import Path

import jsonlines
from jsonlines import jsonlines

from singleton_meta import SingletonMeta
from logger import get_logger
from streamer import Streamer

logger = get_logger('data_handler')


class DataHandler(metaclass=SingletonMeta):
    def __init__(self):
        self.streamers = self.load_streamers()

    def load_streamers(self) -> list[Streamer]:
        # Read followed streamers data file
        logger.info("Retrieving streamers")
        streamers: list[Streamer] = []
        with open("../data/setup.json", "r") as file:
            data = json.load(file)
            for record in data:
                streamers.append(Streamer(record))
        return streamers

    def get_streamer(self, streamer_name: str) -> Streamer | None:
        for stream in self.streamers:
            if stream.name == streamer_name:
                return stream
        return None

    def get_streamers(self) -> list[Streamer]:
        return self.streamers

    def add_stream_log(self, streamer: str, start_time: datetime, end_time: datetime):
        stream_dir = Path(f"../data/{streamer}")
        stream_dir.mkdir(parents=True, exist_ok=True)
        stream_file = Path(f"{stream_dir}/streams.jsonl")
        stream_file.touch()
        with jsonlines.open(stream_file, mode="a") as writer:
            writer.write({"start_time": str(start_time), "end_time": str(end_time)})

