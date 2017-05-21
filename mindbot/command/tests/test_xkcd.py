from json import dumps
from requests import ConnectionError
import requests_mock
from unittest.mock import MagicMock, Mock

from mindbot.command.comics.xkcd import XkcdCommand
from mindbot.router import CommandRouter
from .fixtures import fake_command_message, fake_xkcd    # noqa: F401

xkcd = XkcdCommand(CommandRouter, '', {})


def test_json_without_query():
    with requests_mock.mock() as m:
        m.get('https://xkcd.com/info.0.json', text=dumps(fake_xkcd()))
        assert xkcd.get_json() == fake_xkcd()


def test_json_with_query():
    xkcd_query = XkcdCommand(CommandRouter, '123', {})
    with requests_mock.mock() as m:
        m.get('http://xkcd.com/123/info.0.json', text=dumps(fake_xkcd()))
        assert xkcd_query.get_json() == fake_xkcd()


def test_get_json_connection_error():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, exc=ConnectionError)
        assert not xkcd.get_json()


def test_get_json_status_code_not_ok():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text='Not found', status_code=404)
        assert not xkcd.get_json()


def test_call_with_json(fake_command_message):    # noqa: F811
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=dumps(fake_xkcd()))
        xkcd.send_telegram_message = MagicMock()
        xkcd()
        mock_response = XkcdCommand.XKCD_TEXT.format(response=fake_xkcd())
        xkcd.send_telegram_message.assert_called_with(mock_response)


def test_call_without_json(fake_command_message):    # noqa: F811
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=dumps(fake_xkcd()))
        xkcd.send_telegram_message = MagicMock()
        xkcd.get_json = Mock(return_value=None)
        xkcd()
        xkcd.send_telegram_message.assert_called_with('No such xkcd strip.')
