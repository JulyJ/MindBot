from json import loads
import requests_mock

from mindbot.telegram import TelegramClient
from mindbot.config import TELEGRAM_TOKEN

UPDATE = '{"ok":true,"result":{"id":228,"first_name":"MindDumpBot","username":"MindDumpBot"}}'

client = TelegramClient(TELEGRAM_TOKEN)


def test_get():
    with requests_mock.mock() as m:
        m.get('https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_TOKEN),
              text=UPDATE)
        assert client.get('getUpdates', {}).text == UPDATE


def test_get_text():
    with requests_mock.mock() as m:
        m.get('https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_TOKEN),
              text=UPDATE)
        assert client.get_text('getUpdates', {}) == UPDATE


def test_get_json():
    with requests_mock.mock() as m:
        m.get('https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_TOKEN),
              text=UPDATE)
        assert client.get_json('getUpdates', {}) == loads(UPDATE)
