from json import dumps
from requests import ConnectionError
import requests_mock
from unittest.mock import MagicMock

from mindbot.command.nasa.asteroid import AsteroidCommand
from mindbot.router import CommandRouter
from .fixtures import fake_asteroid_message

instance = AsteroidCommand(CommandRouter, '', {})
ASTEROID_TEXT = (
        'Name: [test](http://test.url)\n'
        'Absolute Magnitude: 1234.43\n'
        'Minimum Diameter: 12\n'
        'Maximum Diameter: 24\n'
        'Hazardous? True\n'
        )


def test_json():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=dumps(fake_asteroid_message()))
        assert instance.get_json() == fake_asteroid_message()


def test_get_json_connection_error():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, exc=ConnectionError)
        assert not instance.get_json()


def test_get_json_status_code_not_ok():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text='Not found', status_code=404)
        assert not instance.get_json()


def test_call_with_json():
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value=fake_asteroid_message())
    instance()
    instance.send_telegram_message.assert_called_with(ASTEROID_TEXT)


def test_call_without_json():
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value=None)
    instance()
    instance.send_telegram_message.assert_called_with('Error while processing the request.')
