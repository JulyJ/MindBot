from json import dumps
from requests import ConnectionError
import requests_mock
from unittest.mock import MagicMock

from mindbot.command.nasa.apod import APODCommand
from mindbot.router import CommandRouter
from .fixtures import fake_apod_message

instance = APODCommand(CommandRouter, '', {})
APOD_TEXT = (
        '[Collapse in Hebes Chasma on Mars]'
        '(https://apod.nasa.gov/apod/image/1705/HebesChasma_esa_960.jpg)\n'
        'What\'s happened in Hebes Chasma on Mars?\n'
        '_Copyright: ESA_'
    )


def test_json():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=dumps(fake_apod_message()))
        assert instance.get_json() == fake_apod_message()


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
    instance.get_json = MagicMock(return_value=fake_apod_message())
    instance()
    instance.send_telegram_message.assert_called_with(APOD_TEXT)


def test_call_without_json():
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value=None)
    instance()
    instance.send_telegram_message.assert_called_with('Error while processing the request.')
