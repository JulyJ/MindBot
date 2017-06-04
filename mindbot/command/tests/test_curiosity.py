from json import dumps
from requests import ConnectionError
import requests_mock
from unittest.mock import MagicMock

from mindbot.command.nasa.curiosity import CuriosityCommand
from mindbot.router import CommandRouter
from .fixtures import fake_curiosity_message

instance = CuriosityCommand(CommandRouter, '', {})
CURIOSITY_TEXT = (
        '[2017-04-05](http://test.src)\n'
        'Camera: camera'
        )


def test_json():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=dumps(fake_curiosity_message()))
        assert instance.get_json() == fake_curiosity_message()


def test_get_json_connection_error():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, exc=ConnectionError)
        assert not instance.get_json()


def test_get_json_status_code_not_ok():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text='Not found', status_code=404)
        assert not instance.get_json()


def test_call_with_photos():
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value=fake_curiosity_message())
    instance()
    instance.send_telegram_message.assert_called_with(CURIOSITY_TEXT)


def test_call_without_photos():
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value={'photos': {}})
    instance()
    instance.send_telegram_message.assert_called_with(
        'No photos loaded yet. Try the previous day.'
    )


def test_call_with_digit_quantity():
    instance = CuriosityCommand(CommandRouter, '5', {})
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value=fake_curiosity_message())
    instance()
    assert instance._quantity == 5


def test_call_with_non_digit_quantity():
    instance = CuriosityCommand(CommandRouter, 'test', {})
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value=fake_curiosity_message())
    instance()
    assert instance._quantity == 3
