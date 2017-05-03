from logging import getLogger
from urllib.parse import urlencode

from .config import TELEGRAM_TOKEN
from .telegram import TelegramClient


class CommandBase:
    name = NotImplemented
    prefix = ''
    disable_web_page_preview = 'true'

    def __init__(self, query: str, message: dict):
        self._telegram = TelegramClient(token=TELEGRAM_TOKEN)
        self._query = query
        self._message = message
        self._logger = getLogger(__name__)

    def __call__(self, *args, **kwargs):
        self._logger.debug('Command {0.name} called'.format(self))

    def send_telegram_message(self, text):
        """This method forms url to send message to telegram."""
        self._telegram.get(
            url_name='sendMessage',
            get_params={
                'text': '{0.prefix}{text}'.format(self, text=text),
                'chat_id': self._message['chat']['id'],
                'parse_mode': 'Markdown',
                'disable_web_page_preview': self.disable_web_page_preview
            }
        )


class SearchCommand(CommandBase):
    prefix = '*😎Found:* \n\n'

class CalculateCommand(CommandBase):
    prefix = '*⚙ Calculated:* \n\n'
