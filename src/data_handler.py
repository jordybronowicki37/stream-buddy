import json

from src.streamer import Streamer


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

