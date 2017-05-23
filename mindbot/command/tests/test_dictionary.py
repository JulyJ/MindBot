from json import dumps
import requests_mock
from unittest.mock import MagicMock

from mindbot.command.search.dictionary import DictionaryCommand
from mindbot.router import CommandRouter
from .fixtures import (fake_dict, fake_empty_senses, fake_empty_entries,
                       fake_empty_lexical_entries, fake_empty_results)

oxford = DictionaryCommand(CommandRouter, 'horse', {})


def test_get_json():
    with requests_mock.mock() as m:
        m.get('https://od-api.oxforddictionaries.com:443/api/v1/entries/en/horse',
              text=dumps(fake_dict()))
        assert oxford.get_json() == fake_dict()


def test_get_json_status_code_not_ok():
    with requests_mock.mock() as m:
        m.get('https://od-api.oxforddictionaries.com:443/api/v1/entries/en/horse',
              status_code=403)
        assert not oxford.get_json()


def test_get_definitions():
    assert oxford.get_definitions(fake_dict()) == ['definition']


def test_get_no_definitions():
    assert oxford.get_definitions(fake_dict()) == ['definition']


def test_get_empty_senses():
    assert not oxford.get_definitions(fake_empty_senses())


def test_get_get_empty_entries():
    assert not oxford.get_definitions(fake_empty_entries())


def test_get_empty_lexical_entries():
    assert not oxford.get_definitions(fake_empty_lexical_entries())


def test_get_empty_results():
    assert not oxford.get_definitions(fake_empty_results())


def test_call_without_query():
    oxford = DictionaryCommand(CommandRouter, '', {})
    oxford.send_telegram_message = MagicMock()
    oxford()
    oxford.send_telegram_message.assert_called_with('Please specify query')


def test_call_without_json():
    oxford.get_json = MagicMock(return_value=None)
    oxford.send_telegram_message = MagicMock()
    oxford()
    oxford.send_telegram_message.assert_called_with('No definitions were found')


def test_call_with_json():
    oxford.get_json = MagicMock(return_value=fake_dict())
    oxford.send_telegram_message = MagicMock()
    oxford()
    oxford.send_telegram_message.assert_called_with("*Definition:* definition\n")
