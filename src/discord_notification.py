import os
import requests

from streamer import Streamer


def send_online_notification(streamer: Streamer):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    requests.post(webhook_url, json={
        'content': f'Streamer {streamer.name} is live!\nView here: {streamer.url}'
    })


def send_offline_notification(streamer: Streamer):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    requests.post(webhook_url, json={
        'content': f'Streamer {streamer.name} is offline!'
    })
