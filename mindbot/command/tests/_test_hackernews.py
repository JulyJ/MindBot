from ..hacker_news.hackernews import NewsCommand
from mindbot.router import CommandRouter

command = NewsCommand(CommandRouter, '', {})


def test_ok_item():
    assert command._get_item('1')


def test_empty_item():
    assert command._get_item('')


def test_non_numeric_item():
    assert command._get_item('wer')


def test_space_item():
    assert command._get_item(' ')


def test_make_text():
    assert command.make_text([1, 'wer', ' ', '', None], '')
