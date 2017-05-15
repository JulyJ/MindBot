import pytest
import json
import requests_mock

from mindbot.bot import MindBot
from mindbot.telegram import TelegramClient
from mindbot.config import TELEGRAM_TOKEN

bot = MindBot()
client = TelegramClient(TELEGRAM_TOKEN)


@pytest.fixture()
def fake_user():
    return {
        "id": 175113727,
        "first_name": "FirstName",
        "last_name": "LastName",
        "username": "UserName"
        }


@pytest.fixture()
def test_chat():
    return {
        "id": 175113727,
        "first_name": "Julia",
        "last_name": "K",
        "username": "JulikSp",
        "type": "private"
        }


@pytest.fixture()
def fake_entities():
    return [{
        "type": "bot_command",
        "offset": 0,
        "length": 5
        }]


@pytest.fixture()
def fake_command_message():
    return {
        "message_id": 1486,
        "from": fake_user(),
        "chat": test_chat(),
        "date": 1494875753,
        "text": '/help',
        "entities": fake_entities()
        }


@pytest.fixture()
def fake_result_message():
    return {
        "update_id": 547461412,
        "message": fake_command_message()
        }


@pytest.fixture()
def fake_updates():
    return {
        "ok": "true",
        "result": [fake_result_message()]
    }


def test_get_updates():
    with requests_mock.mock() as m:
        m.get('https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_TOKEN),
              text=json.dumps(fake_updates()))
        assert bot.get_updates() == [fake_result_message()]
