from os import getenv
import requests

from streamer import Streamer


def send_online_notification(streamer: Streamer):
    if not streamer.notify_when_online:
        return
    webhook_url = getenv("DISCORD_WEBHOOK_URL")
    viewHereText = f"\nView here: {streamer.url}"
    requests.post(webhook_url, json={
        "content": f"Streamer {streamer.name} is live!{viewHereText if streamer.show_url else ''}",
    })


def send_offline_notification(streamer: Streamer):
    if not streamer.notify_when_offline:
        return
    webhook_url = getenv("DISCORD_WEBHOOK_URL")
    requests.post(webhook_url, json={
        "content": f"Streamer {streamer.name} is offline!"
    })
