from ..search.urban import UrbanDictionaryCommand
from mindbot.router import CommandRouter

command = UrbanDictionaryCommand(CommandRouter, '', {})


def test_ok_item():
    assert command.get_definition('horse')


def test_empty_item():
    assert command.get_definition('')


def test_space_item():
    assert command.get_definition('horse tag')


def test_comma_item():
    assert command.get_definition('horse,tag')


def test_none_item():
    assert command.get_definition(None)


def test_integer_item():
    assert command.get_definition(123)
