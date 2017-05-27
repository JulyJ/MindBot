"""
    This module serves commands to Hacker News API.

    More information about API can be found here https://github.com/HackerNews/API.
    Module provide responses for 3 commands available to user:
        - /latestnews
        - /topnews
        - /bestnews
    Bot will retrieve list of news and then send specified amount of title, links
    and rating to user, default amount of news items is 10.

    Example:
        /latestnews 10
"""

from requests import get

from ..commandbase import CommandBase


NEWS_TEXT = '📄 *{item[title]}* [Read more...]({item[url]}) Score: *{item[score]}*\n'


class NewsCommand(CommandBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._query.isdigit():
            self._quantity = int(self._query)
        else:
            self._quantity = 10

    @staticmethod
    def _get_latest_items(request_type):
        url = 'https://hacker-news.firebaseio.com/v0/{}'.format(request_type)
        response = get(url)
        return response.json()

    @staticmethod
    def _get_item(item_id):
        url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(item_id)
        response = get(url).json()
        return {
            'title': response.get('title'),
            'url': response.get('url'),
            'score': response.get('score'),
        }

    def make_text(self, news_ids, text):
        items = map(self._get_item, news_ids)
        return text + ''.join(NEWS_TEXT.format(item=item) for item in items)


class LatestNewsCommand(NewsCommand):
    name = '/latestnews'
    help_text = '<N> - Gets N latest Hacker News stories.'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = 'Latest {} Hacker News stories: \n\n'.format(self._quantity)
        news_ids = self._get_latest_items('newstories.json')[:self._quantity]
        text = self.make_text(news_ids, text)
        self.send_telegram_message(text)


class TopNewsCommand(NewsCommand):
    name = '/topnews'
    help_text = '<N> - Gets N top Hacker News stories.'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = 'Top {} Hacker News stories: \n\n'.format(self._quantity)
        news_ids = self._get_latest_items('topstories.json')[:self._quantity]
        text = self.make_text(news_ids, text)
        self.send_telegram_message(text)


class BestNewsCommand(NewsCommand):
    name = '/bestnews'
    help_text = '<N> - Gets N best Hacker News stories.'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = 'Best {} Hacker News stories: \n\n'.format(self._quantity)
        news_ids = self._get_latest_items('beststories.json')[:self._quantity]
        text = self.make_text(news_ids, text)
        self.send_telegram_message(text)
