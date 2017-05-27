"""
    Module provide parent classes for received commands.

    CommandBase is core method that sets variables parsed from message and
    prepares template telegram message for response. Supplementary classes
    inherited from CommandBase class add some command-specific response prefixes.
"""

from logging import getLogger

from mindbot.config import TELEGRAM_TOKEN
from mindbot.telegram import TelegramClient


class CommandBase:
    name = NotImplemented
    help_text = NotImplemented
    prefix = ''
    disable_web_page_preview = 'true'

    def __init__(self, router, query: str, message: dict):
        self._router = router
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
