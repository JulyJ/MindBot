from unittest.mock import MagicMock


from mindbot.command.remember.searchtag import SearchTagCommand
from mindbot.command.remember.db import DataBaseConnection
from mindbot.router import CommandRouter


def test_call_with_query():
    instance = SearchTagCommand(CommandRouter, '', {})
    instance.send_telegram_message = MagicMock()
    instance()
    instance.send_telegram_message.assert_called_with('Please specify #tags')


def test_call_with_no_tags():
    instance = SearchTagCommand(CommandRouter, 'test', {})
    instance.send_telegram_message = MagicMock()
    instance()
    instance.send_telegram_message.assert_called_with('Please specify #tags')


def test_no_records():
    instance = SearchTagCommand(CommandRouter, '#tag', {})
    DataBaseConnection.search_messages = MagicMock(return_value=None)
    instance.send_telegram_message = MagicMock()
    instance()
    DataBaseConnection.search_messages.assert_called_with('#tag')
    instance.send_telegram_message.assert_called_with('No records for #tag')


def test_records_found():
    instance = SearchTagCommand(CommandRouter, '#tag', {})
    DataBaseConnection.search_messages = MagicMock(return_value=['text'])
    instance.send_telegram_message = MagicMock()
    instance()
    DataBaseConnection.search_messages.assert_called_with('#tag')
    instance.send_telegram_message.assert_called_with('text')
