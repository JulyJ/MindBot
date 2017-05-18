from unittest.mock import MagicMock

from mindbot.telegram import TelegramClient
from mindbot.config import TELEGRAM_TOKEN

client = TelegramClient(TELEGRAM_TOKEN)


def test_get():
    http_get = MagicMock()
    client.get('getUpdates', {})
    http_get.assert_called_with('https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_TOKEN))
