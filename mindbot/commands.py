from datetime import datetime
from logging import getLogger
from re import compile as re_compile
from typing import Any, Dict, List
from urllib.parse import urlencode

from pyowm import OWM, exceptions as owm_exceptions
from wikipedia import exceptions as wiki_exceptions, page as wiki_page

from .config import db_connection_string, TELEGRAM_TOKEN, WEATHER_TOKEN
from .texts import HELP_TEXT, WEATHER_TEXT, GREETINGS_TEXT
from .db import DataBaseConnection
from .telegram import TelegramClient


def parse_tags(text) -> List[str]:
    tags_finder = re_compile(r'#[^\s]+')
    return tags_finder.findall(text)


class CommandBase:
    name = NotImplemented
    prefix = ''

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
            }
        )


class SearchCommand(CommandBase):
    prefix = '😎Found: \n\n'

class GoogleCommand(SearchCommand):
    name = '/google'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            query = urlencode({'btnI': 'I', 'q': self._query})
            url = 'http://www.google.com/search?' + query
            return self.send_telegram_message(url)
        else:
            return self.send_telegram_message('Please specify query')

class WikiCommand(SearchCommand):
    name = '/wiki'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            try:
                page = wiki_page(self._query)
            except wiki_exceptions.PageError:
                self.send_telegram_message('No such page 😭')
            except wiki_exceptions.WikipediaException:
                self.send_telegram_message('Error while processing request 😭')
            else:
                self.send_telegram_message('{p.title} {p.url}'.format(p=page))
        else:
            return self.send_telegram_message('Please specify query')

class GreetingsCommand(CommandBase):
    name = '/start'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = GREETINGS_TEXT.format(f=self._message['from'])
        self.send_telegram_message(text=text)


class HelpCommand(CommandBase):
    name = '/help'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = HELP_TEXT.format(f=self._message['from'])
        self.send_telegram_message(text=text)


class WeatherCommand(CommandBase):
    name = '/weather'
    prefix = '🌤  Current weather: \n\n'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            try:
                observation = OWM(WEATHER_TOKEN).weather_at_place(self._query)
            except owm_exceptions.OWMError:
                self.send_telegram_message('No such location 😭')
            else:
                weather = observation.get_weather()
                city = observation.get_location().get_name()
                status = weather.get_status()
                temperature = weather.get_temperature('celsius')
                wind = weather.get_wind()
                humidity = weather.get_humidity()
                pressure = weather.get_pressure()
                text = WEATHER_TEXT.format(city, status, temperature['temp'], wind['speed'], humidity, pressure['press'])
                return self.send_telegram_message(text=text)
        else:
            return self.send_telegram_message('Please pecify location')

class SearchTagCommand(SearchCommand):
    name = '/search'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._database = DataBaseConnection(db_connection_string)

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            tags = parse_tags(self._message['text'])
            for tag in tags:
                with self._database as db:
                    messages = db.search_messages(tag)
                    if len(messages) > 0:
                        for message in messages:
                            self.send_telegram_message(message)
                    else:
                        self.send_telegram_message('No records for {}'.format(tag))
        else:
            return self.send_telegram_message('Please pecify #tags')


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
                tags=parse_tags(self._message['text']),
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


class CommandRouter:
    command_class_mapper = {
        '/wiki': WikiCommand,
        '/google': GoogleCommand,
        '/start': GreetingsCommand,
        '/weather': WeatherCommand,
        '/help': HelpCommand,
        '/search': SearchTagCommand,
        None: RememberAll}


    @classmethod
    def route(cls, message: Dict[str, Any]):
        command, _, query = message['text'].partition(' ')
        command = command.lower()
        if command not in cls.command_class_mapper:
            command = None
        command_class = cls.command_class_mapper.get(command, None)
        command_instance = command_class(query, message)
        return command_instance()

