from ..search.dictionary import DictionaryCommand
from mindbot.router import CommandRouter


def test_ok():
    command = DictionaryCommand(CommandRouter, 'test', {})
    assert command.get_json()


def test_two_entries():
    command = DictionaryCommand(CommandRouter, 'golden gate', {})
    assert command.get_json()


def test_empty():
    command = DictionaryCommand(CommandRouter, '', {})
    assert not command.get_json()


def test_space():
    command = DictionaryCommand(CommandRouter, ' ', {})
    assert not command.get_json()


def test_numeric():
    command = DictionaryCommand(CommandRouter, '123', {})
    assert not command.get_json()
