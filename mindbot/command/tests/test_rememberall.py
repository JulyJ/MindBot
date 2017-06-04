from unittest.mock import Mock

from mindbot.command.remember.rememberall import RememberAll
from mindbot.router import CommandRouter


def test_call_without_query():
    instance = RememberAll(CommandRouter, '', {})
    instance.send_telegram_message = Mock()
    instance()
    instance.send_telegram_message.assert_called_with('Please specify message to remember.')
