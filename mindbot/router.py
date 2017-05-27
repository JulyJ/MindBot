"""
    Module designed to route messages based on strategy pattern.

    This module includes class mapper tuple to correlate received from telegram
    user command with target command class to run. Additionally, this module
    generates help message based on command list.
"""

from typing import Any, Dict

from .command.help.commands import GreetingsCommand, HelpCommand
from .command.nasa.apod import APODCommand
from .command.nasa.asteroid import AsteroidCommand
from .command.nasa.curiosity import CuriosityCommand
from .command.search.google import GoogleCommand
from .command.search.wiki import WikiCommand, RandomCommand
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
from .command.news.hackernews import LatestNewsCommand, TopNewsCommand, BestNewsCommand
from .command.news.canadanews import CanadaStatsCommand


class CommandRouter:
    command_class_mapper = (
        ('/help', HelpCommand),
        ('/asteroid', AsteroidCommand),
        ('/start', GreetingsCommand),
        ('/canadastat', CanadaStatsCommand),
        ('/oxford', DictionaryCommand),
        ('/exchange', ExchangeCommand),
        ('/forecast', ForecastCommand),
        ('/google', GoogleCommand),
        ('/search', SearchTagCommand),
        ('/urban', UrbanDictionaryCommand),
        ('/weather', WeatherCommand),
        ('/curiosity', CuriosityCommand),
        ('/qr', QrCommand),
        ('/ocr', OcrCommand),
        ('/apod', APODCommand),
        ('/wiki', WikiCommand),
        ('/random', RandomCommand),
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
        if command not in dict(cls.command_class_mapper):
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
