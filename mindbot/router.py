from typing import Any, Dict

from .command.help.commands import GreetingsCommand, HelpCommand
from .command.search.google import GoogleCommand
from .command.search.wiki import WikiCommand
from .command.weather.weather import WeatherCommand
from .command.weather.forecast import ForecastCommand
from .command.exchange.exchange import ExchangeCommand
from .command.remember.rememberall import RememberAll
from .command.remember.searchtag import SearchTagCommand

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

