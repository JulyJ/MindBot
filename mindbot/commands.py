from datetime import datetime
from logging import getLogger
from re import compile as re_compile, search as re_search
from typing import Any, Dict, List
from urllib.parse import urlencode

from pyowm import OWM, exceptions as owm_exceptions
from wikipedia import exceptions as wiki_exceptions, page as wiki_page

from .config import db_connection_string, TELEGRAM_TOKEN, WEATHER_TOKEN
from .db import DataBaseConnection
from .exchangerates import OpenExchangeRatesClient
from .telegram import TelegramClient
from .texts import HELP_TEXT, WEATHER_TEXT, GREETINGS_TEXT, FORECAST_TEXT


def parse_tags(text) -> List[str]:
    tags_finder = re_compile(r'#[^\s]+')
    return tags_finder.findall(text)


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

class ExchangeCommand(CalculateCommand):
    name = '/exchange'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._exchange = OpenExchangeRatesClient()

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self.currency_parser(self._query):
            params = self._query.split(' ')
            rate = self._exchange.get_rate(params[1], params[2])
            if rate is not None:
                return self.send_telegram_message("*{}* {} = *{}* {}".format(
                    params[0],
                    params[1],
                    round(rate*float(params[0]), 2),
                    params[2]
                ))
            else:
                return self.send_telegram_message('Please specify existing currency')
        else:
                return self.send_telegram_message('Please specify query as ```<amount> <base currency> <target currency>```')

    def currency_parser(self, text) -> List[str]:
        return re_search(r'([0-9]+)\s([a-zA-Z]{3})\s([a-zA-Z]{3})', text)



class GoogleCommand(SearchCommand):
    name = '/google'
    disable_web_page_preview = 'false'

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
                content = page.content[:512]
                self.send_telegram_message('*{p.title}* \n\n{}...\n\n[Read more at Wikipedia]({p.url})'.format(content, p=page))
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


class ForecastCommand(CommandBase):
    name = '/forecast'
    prefix = '🌤  *3-days forecast:* \n'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            try:
                forecast = OWM(WEATHER_TOKEN).daily_forecast(self._query, limit=3)
            except owm_exceptions.OWMError:
                self.send_telegram_message('No such location 😭')
            else:
                weathers = forecast.get_forecast()
                for weather in weathers.get_weathers():
                    city = weathers.get_location().get_name()
                    date = weather.get_reference_time('iso')
                    status = weather.get_status()
                    temperature = weather.get_temperature('celsius')
                    wind = weather.get_wind()
                    text = FORECAST_TEXT.format(date, city, status, temperature['day'], temperature['night'], wind['speed'])
                    self.send_telegram_message(text=text)
        else:
            return self.send_telegram_message('Please pecify location')


class WeatherCommand(CommandBase):
    name = '/weather'
    owm_emoji_map = {
        '01d': '☀️',
        '01n': '☀️',
        '02d': '🌤',
        '02n': '🌤',
        '03d': '⛅️',
        '03n': '⛅️',
        '04d': '🌥',
        '04n': '🌥',
        '09d': '🌧',
        '09n': '🌧',
        '10d': '🌦',
        '10n': '🌦',
        '11d': '⛈',
        '11n': '⛈',
        '13d': '🌨',
        '13n': '🌨',
        '50d': '🌫',
        '50n': '🌫'
    }
    prefix = 'Current weather: \n\n'

    def get_emoji(self, weather):
        iconId = weather.get_weather_icon_name()
        if (self.owm_emoji_map[iconId]):
            return self.owm_emoji_map[iconId]

        return ''
    prefix = ' *Current weather:* \n\n'

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
                self.prefix = self.get_emoji(weather) + ' ' + self.prefix
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
    prefix = '*😎Remebered:* \n\n'

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
        '/exchange': ExchangeCommand,
        '/forecast': ForecastCommand,
        '/google': GoogleCommand,
        '/help': HelpCommand,
        '/search': SearchTagCommand,
        '/start': GreetingsCommand,
        '/weather': WeatherCommand,
        '/wiki': WikiCommand,
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

