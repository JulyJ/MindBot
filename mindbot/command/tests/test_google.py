from unittest.mock import MagicMock
from urllib.parse import urlencode

from mindbot.command.search.google import GoogleCommand
from mindbot.router import CommandRouter

instance = GoogleCommand(CommandRouter, "test", {})


def test_call_without_query():
    instance = GoogleCommand(CommandRouter, "", {})
    instance.send_telegram_message = MagicMock()
    instance()
    instance.send_telegram_message.assert_called_with('Please specify query')


def test_call_ok():
    instance.send_telegram_message = MagicMock()
    instance()
    query = urlencode({'btnI': 'I', 'q': 'test'})
    instance.send_telegram_message.assert_called_with('http://www.google.com/search?' + query)
