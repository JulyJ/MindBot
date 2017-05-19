import json
import requests_mock
from unittest.mock import MagicMock

from mindbot.bot import MindBot
from mindbot.router import CommandRouter
from mindbot.telegram import TelegramClient
from mindbot.config import TELEGRAM_TOKEN
from .fixtures import (fake_updates, fake_result_message,    # noqa: F401
                       fake_empty_updates, fake_commands_message)

bot = MindBot()
router = CommandRouter()
client = TelegramClient(TELEGRAM_TOKEN)


def test_get_updates():
    with requests_mock.mock() as m:
        m.get('https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_TOKEN),
              text=json.dumps(fake_updates()))
        assert bot.get_updates() == [fake_result_message()]


def test_get_empty_updates():
    with requests_mock.mock() as m:
        m.get('https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_TOKEN),
              text=json.dumps(fake_empty_updates()))
        assert bot.get_updates() == []


def test_set_last_update_id():
    with requests_mock.mock() as m:
        m.get('https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_TOKEN),
              text=json.dumps(fake_updates()))
        bot.set_last_update_id([fake_result_message()])
        assert bot._last_update_id == 547461412 + 1


def test_route_message(fake_commands_message):    # noqa: F811
    CommandRouter.route = MagicMock()
    bot.route_message(fake_commands_message)
    CommandRouter.route.assert_called_with(fake_commands_message[0]['message'])
