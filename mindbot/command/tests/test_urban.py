from json import dumps
from requests import ConnectionError
import requests_mock
from unittest.mock import MagicMock, Mock

from mindbot.command.search.urban import UrbanDictionaryCommand
from mindbot.router import CommandRouter
from .fixtures import fake_empty_urban, fake_urban

urban = UrbanDictionaryCommand(CommandRouter, 'horse', {})


def test_get_definition():
    with requests_mock.mock() as m:
        m.get('http://api.urbandictionary.com/v0/define?term=horse', text=dumps(fake_urban()))
        assert urban.get_definition() == fake_urban()['list']


def test_get_definition_connection_error():
    with requests_mock.mock() as m:
        m.get('http://api.urbandictionary.com/v0/define?term=horse', exc=ConnectionError)
        assert not urban.get_definition()


def test_get_definition_status_code_not_ok():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text='Not found', status_code=404)
        assert not urban.get_definition()


def test_call_with_query():
    urban.send_telegram_message = MagicMock()
    urban.get_definition = MagicMock(return_value=fake_urban()['list'])
    urban()
    urban.send_telegram_message.assert_called_with(urban.URBAN_TEXT.format(
        definition=fake_urban()['list'][0]))


def test_call_without_query():
    urban_empty = UrbanDictionaryCommand(CommandRouter, '', {})
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=dumps(fake_urban()))
        urban_empty.send_telegram_message = MagicMock()
        urban_empty.get_json = Mock(return_value=fake_urban())
        urban_empty()
        urban_empty.send_telegram_message.assert_called_with('Please specify query')


def test_call_without_definitions():
    urban.send_telegram_message = MagicMock()
    urban.get_definition = MagicMock(return_value=fake_empty_urban()['list'])
    urban()
    urban.send_telegram_message.assert_called_with('No definitions were found')
