import pytest
import json
import requests_mock
from unittest.mock import MagicMock

from mindbot.bot import MindBot
from mindbot.router import CommandRouter
from mindbot.telegram import TelegramClient
from mindbot.config import TELEGRAM_TOKEN

bot = MindBot()
router = CommandRouter()
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


def get_commands():
    commands_list = []
    for command in CommandRouter.get_commands_help():
        commands_list.append(command[0])
    return commands_list


@pytest.fixture(params=get_commands())
def fake_commands_message(request):
    return [{
        "update_id": 547461412,
        "message": {
            "message_id": 1486,
            "from": fake_user(),
            "chat": test_chat(),
            "date": 1494875753,
            "text": request.param,
            "entities": fake_entities()
            }
        }]


@pytest.fixture()
def fake_updates():
    return {
        "ok": "true",
        "result": [fake_result_message()]
    }


@pytest.fixture()
def fake_command_updates():
    return {
        "ok": "true",
        "result": fake_commands_message()
    }


@pytest.fixture()
def fake_empty_updates():
    return {
        "ok": "true",
        "result": []
    }


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


def test_route_message(fake_commands_message):
    CommandRouter.route = MagicMock()
    bot.route_message(fake_commands_message)
    CommandRouter.route.assert_called_with(fake_commands_message[0]['message'])
