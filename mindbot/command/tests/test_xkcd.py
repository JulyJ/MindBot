from ..comics.xkcd import XkcdCommand
from mindbot.router import CommandRouter

def test_empty():
    command = XkcdCommand(CommandRouter, '', {})
    assert command.get_json()

def test_numeric():
    command = XkcdCommand(CommandRouter, '123', {})
    assert command.get_json()


def test_big_numeric():
    command = XkcdCommand(CommandRouter, '9999999', {})
    assert not command.get_json()


def test_char():
    command = XkcdCommand(CommandRouter, 'test', {})
    assert not command.get_json()


def test_space():
    command = XkcdCommand(CommandRouter, ' ', {})
    assert not command.get_json()