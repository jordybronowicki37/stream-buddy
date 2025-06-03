import os
import requests


def send_online_notification(name):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    requests.post(webhook_url, json={
        'content': f'Streamer {name} is live!'
    })


def send_offline_notification(name):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    requests.post(webhook_url, json={
        'content': f'Streamer {name} is offline!'
    })
