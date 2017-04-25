from datetime import datetime
from logging import getLogger
from re import compile as re_compile
from typing import Any, Dict, List
from urllib.parse import urlencode

from wikipedia import exceptions as wiki_exceptions, page as wiki_page

from .config import db_connection_string, telegram_token
from .db import DataBaseConnection
from .telegram import TelegramClient


class CommandRouter:
    command_class_mapper = {}

    @classmethod
    def route(cls, message: Dict[str, Any]):
        command, _, query = message['text'].partition(' ')
        command_class = cls.command_class_mapper.get(command, None)
        command_instance = command_class(query, message)
        return command_instance()


class CommandMeta(type):
    def __init__(cls, cls_name, bases, attrs):
        name = attrs.get('name', NotImplemented)
        if name is not NotImplemented:
            CommandRouter.command_class_mapper[name] = cls
        super().__init__(cls_name, bases, attrs)


class CommandBase(metaclass=CommandMeta):
    name = NotImplemented
    prefix = ''

    def __init__(self, query: str, message: dict):
        self._telegram = TelegramClient(token=telegram_token)
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
            }
        )


class SearchCommand(CommandBase):
    prefix = '😎Found: \n\n'


class GoogleCommand(SearchCommand):
    name = 'google'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        query = urlencode({'btnI': 'I', 'q': self._query})
        url = 'http://www.google.com/search?' + query
        return self.send_telegram_message(url)


class WikiCommand(SearchCommand):
    name = 'wiki'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        try:
            page = wiki_page(self._query)
        except wiki_exceptions.PageError:
            self.send_telegram_message('No such page 😭')
        except wiki_exceptions.WikipediaException:
            self.send_telegram_message('Error while processing request 😭')
        else:
            self.send_telegram_message('{p.title} {p.url}'.format(p=page))


class GreetingsCommand(CommandBase):
    name = '/start'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = (
            'Greetings, {from[first_name]} {from[last_name]}.\n\n'
            'This is MindDumpBot. '
            'He can google something for you or search in wikipedia. '
            'Use "wiki <text>" or "google <text>" commands. '
            'Also it can remember all your messages, use #tags! \n\n'
            'Have a nice day!'
        ).format(f=self._message['from'])
        self.send_telegram_message(text=text)


class RememberAll(CommandBase):
    name = None
    prefix = '😎Remebered: \n\n'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._database = DataBaseConnection(db_connection_string)

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        with self._database as db:
            db.add_message(
                text=self._message['text'],
                date=self.date,
                sender=self.sender,
                tags=self.parse_tags(),
            )
        self.send_telegram_message(self._message['text'])

    @property
    def sender(self):
        return '{0[first_name]} {0[last_name]}'.format(self._message['from'])

    @property
    def date(self) -> datetime:
        """This method convert unixtime date to human-readable format"""
        timestamp = int(self._message['date'])
        return datetime.fromtimestamp(timestamp)

    def parse_tags(self) -> List[str]:
        tags_finder = re_compile(r'#[^\s]+')
        return tags_finder.findall(self._message['text'])
