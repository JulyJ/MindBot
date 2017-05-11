from typing import Any, Dict

from .command.help.commands import GreetingsCommand, HelpCommand
from .command.search.google import GoogleCommand
from .command.search.wiki import WikiCommand
from .command.search.urban import UrbanDictionaryCommand
from .command.search.dictionary import DictionaryCommand
from .command.weather.weather import WeatherCommand
from .command.weather.forecast import ForecastCommand
from .command.exchange.exchange import ExchangeCommand
from .command.remember.rememberall import RememberAll
from .command.remember.searchtag import SearchTagCommand
from .command.comics.xkcd import XkcdCommand
from .command.tools.qrgenerator import QrCommand
from .command.tools.ocr import OcrCommand
from .command.hacker_news.hackernews import LatestNewsCommand, TopNewsCommand, BestNewsCommand


class CommandRouter:
    command_class_mapper = (
        ('/help', HelpCommand),
        ('/start', GreetingsCommand),
        ('/oxford', DictionaryCommand),
        ('/exchange', ExchangeCommand),
        ('/forecast', ForecastCommand),
        ('/google', GoogleCommand),
        ('/search', SearchTagCommand),
        ('/urban', UrbanDictionaryCommand),
        ('/weather', WeatherCommand),
        ('/qr', QrCommand),
        ('/ocr', OcrCommand),
        ('/wiki', WikiCommand),
        ('/xkcd', XkcdCommand),
        ('/latestnews', LatestNewsCommand),
        ('/topnews', TopNewsCommand),
        ('/bestnews', BestNewsCommand),
        ('/remember', RememberAll),
    )

    @classmethod
    def route(cls, message: Dict[str, Any]):
        command, _, query = message['text'].partition(' ')
        command = command.lower()
        if command not in cls.command_class_mapper:
            return
        command_class = dict(cls.command_class_mapper).get(command, None)
        command_instance = command_class(cls, query, message)
        return command_instance()

    @classmethod
    def get_commands_help(cls):
        return (
            (command, command_class.help_text)
            for command, command_class in cls.command_class_mapper
            if command_class.help_text is not None
        )
