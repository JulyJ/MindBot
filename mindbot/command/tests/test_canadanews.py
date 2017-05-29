from json import dumps
import requests_mock
from requests import ConnectionError
from unittest.mock import MagicMock

from mindbot.command.news.canadanews import CanadaStatsCommand
from mindbot.router import CommandRouter
from .fixtures import fake_canadanews, fake_canadanews_article

instance = CanadaStatsCommand(CommandRouter, "", {})


def test_get_json():
    with requests_mock.mock() as m:
        m.get('http://www.statcan.gc.ca/sites/json/daily-banner-eng.json',
              text=dumps(fake_canadanews()))
        assert instance.get_json() == fake_canadanews()


def test_get_json_status_code_not_ok():
    with requests_mock.mock() as m:
        m.get('http://www.statcan.gc.ca/sites/json/daily-banner-eng.json',
              status_code=404)
        assert not instance.get_json()


def test_get_json_connection_error():
    with requests_mock.mock() as m:
        m.get('http://www.statcan.gc.ca/sites/json/daily-banner-eng.json',
              exc=ConnectionError)
        assert not instance.get_json()


def test_call_with_json():
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value=fake_canadanews())
    instance()
    instance.send_telegram_message.assert_called_with(
        instance.NEWS_TEXT.format(response=fake_canadanews_article())
        )


def test_call_without_json():
    instance.send_telegram_message = MagicMock()
    instance.get_json = MagicMock(return_value=None)
    instance()
    instance.send_telegram_message.assert_called_with('No news were retrieved.')
