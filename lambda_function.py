import json
import os
import logging

from telegram_client import TelegramClient
from tiktok import download_video
from tiktok import strip_url_params
from tiktok import is_tiktok_url

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

telegram_client = TelegramClient(token=TELEGRAM_TOKEN)


def process_even(event):
    message = json.loads(event['body'])
    logging.info(message)

    chat_id = message['message']['chat']['id']

    if 'text' not in message['message']:
        telegram_client.send_message(chat_id, "Please send valid TikTok url")
        return

    text = message['message']['text']

    if text == "/start":
        telegram_client.send_message(chat_id, "Hi! Send me a TikTok link")
        return

    if not is_tiktok_url(text):
        telegram_client.send_message(chat_id, "Please send valid TikTok url")
        return

    url = strip_url_params(text)
    logger.info("Downloading video from %s", url)

    telegram_client.send_message(chat_id, "Downloading your TikTok, please wait a moment")
    video_file = download_video(url)
    telegram_client.send_file(chat_id, video_file)


def lambda_handler(event, context):
    process_even(event)
    return {
        'statusCode': 200
    }
