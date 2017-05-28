from unittest.mock import MagicMock

from mindbot.command.tools.qrgenerator import QrCommand
from mindbot.router import CommandRouter

instance = QrCommand(CommandRouter, "test", {})


def test_call_without_query():
    instance = QrCommand(CommandRouter, "", {})
    instance.send_telegram_message = MagicMock()
    instance()
    instance.send_telegram_message.assert_called_with('No query provided.')


def test_call_ok():
    instance.send_telegram_message = MagicMock()
    instance()
    instance.send_telegram_message.assert_called_with('[QR link]({})'.format(instance.form_url))
