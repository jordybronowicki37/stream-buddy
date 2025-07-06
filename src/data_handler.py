import json
from datetime import datetime

import jsonlines

from streamer import Streamer


def get_streamers() -> list[Streamer]:
    streamers: list[Streamer] = []

    with open("data/setup.json", "r") as file:
        data = json.load(file)
        for record in data:
            streamers.append(Streamer(
                record["name"],
                record["url"],
                record["showUrl"],
                record["selector"],
                record["timeout"],
                record["notify_when_online"],
                record["notify_when_offline"]
            ))

    return streamers


def add_stream_log(streamer: str, start_time: datetime, end_time: datetime):
    with jsonlines.open(f"data/{streamer}/streams.jsonl", mode="w") as writer:
        writer.write({"start_time": start_time, "end_time": end_time})

