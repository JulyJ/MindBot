from json import dumps
import requests_mock
from unittest.mock import MagicMock

from mindbot.command.hacker_news.hackernews import (LatestNewsCommand, BestNewsCommand,
                                                    TopNewsCommand, NewsCommand, NEWS_TEXT)
from mindbot.router import CommandRouter
from .fixtures import fake_hknews_list, fake_hknews_item

instance = NewsCommand(CommandRouter, '', {})
latestnews = LatestNewsCommand(instance, '', {})
topnews = TopNewsCommand(instance, '', {})
bestnews = BestNewsCommand(instance, '', {})


def test_get_latest_items():
    with requests_mock.mock() as m:
        m.get('https://hacker-news.firebaseio.com/v0/newstories.json',
              text=dumps(fake_hknews_list()))
        assert latestnews._get_latest_items('newstories.json') == fake_hknews_list()


def test_get_top_items():
    with requests_mock.mock() as m:
        m.get('https://hacker-news.firebaseio.com/v0/topstories.json',
              text=dumps(fake_hknews_list()))
        assert topnews._get_latest_items('topstories.json') == fake_hknews_list()


def test_get_best_items():
    with requests_mock.mock() as m:
        m.get('https://hacker-news.firebaseio.com/v0/beststories.json',
              text=dumps(fake_hknews_list()))
        assert bestnews._get_latest_items('beststories.json') == fake_hknews_list()


def test_get_item():
    with requests_mock.mock() as m:
        m.get('https://hacker-news.firebaseio.com/v0/item/1.json',
              text=dumps(fake_hknews_item()))
        assert latestnews._get_item(1) == fake_hknews_item()
        assert topnews._get_item(1) == fake_hknews_item()
        assert bestnews._get_item(1) == fake_hknews_item()


def test_make_text():
    latestnews._get_item = MagicMock(return_value=fake_hknews_item())
    topnews._get_item = MagicMock(return_value=fake_hknews_item())
    bestnews._get_item = MagicMock(return_value=fake_hknews_item())
    assert latestnews.make_text([1], '') == NEWS_TEXT.format(item=fake_hknews_item())
    assert topnews.make_text([1], '') == NEWS_TEXT.format(item=fake_hknews_item())
    assert bestnews.make_text([1], '') == NEWS_TEXT.format(item=fake_hknews_item())


def test_call_latest_news():
    latestnews._get_latest_items = MagicMock(return_value=fake_hknews_list())
    latestnews.make_text = MagicMock(return_value=NEWS_TEXT.format(item=fake_hknews_item()))
    latestnews.send_telegram_message = MagicMock()
    latestnews()
    latestnews._get_latest_items.assert_called_with('newstories.json')
    latestnews.make_text.assert_called_with(fake_hknews_list(),
                                            'Latest 10 Hacker News stories: \n\n')
    latestnews.send_telegram_message.assert_called_with(NEWS_TEXT.format(item=fake_hknews_item()))


def test_call_top_news():
    topnews._get_latest_items = MagicMock(return_value=fake_hknews_list())
    topnews.make_text = MagicMock(return_value=NEWS_TEXT.format(item=fake_hknews_item()))
    topnews.send_telegram_message = MagicMock()
    topnews()
    topnews._get_latest_items.assert_called_with('topstories.json')
    topnews.make_text.assert_called_with(fake_hknews_list(),
                                         'Top 10 Hacker News stories: \n\n')
    topnews.send_telegram_message.assert_called_with(NEWS_TEXT.format(item=fake_hknews_item()))


def test_call_best_news():
    bestnews._get_latest_items = MagicMock(return_value=fake_hknews_list())
    bestnews.make_text = MagicMock(return_value=NEWS_TEXT.format(item=fake_hknews_item()))
    bestnews.send_telegram_message = MagicMock()
    bestnews()
    bestnews._get_latest_items.assert_called_with('beststories.json')
    bestnews.make_text.assert_called_with(fake_hknews_list(),
                                          'Best 10 Hacker News stories: \n\n')
    bestnews.send_telegram_message.assert_called_with(NEWS_TEXT.format(item=fake_hknews_item()))


def test_call_without_query():
    news_instance = NewsCommand(CommandRouter, '', {})
    assert news_instance._quantity == 10


def test_call_with_query():
    news_instance = NewsCommand(CommandRouter, '5', {})
    assert news_instance._quantity == 5


def test_call_with_not_digit():
    news_instance = NewsCommand(CommandRouter, 'test', {})
    assert news_instance._quantity == 10
