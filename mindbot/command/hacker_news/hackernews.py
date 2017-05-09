from requests import get

from .hackernewsclient import HackerNewsClient
from ..commandbase import CommandBase

NEWS_TEXT = ('📄 *{}* [Read more...]({}) Score: *{}*\n')

class NewsCommand(CommandBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = HackerNewsClient()
        if self._client.is_number(self._query):
            self._quantity = int(self._query)
        else:
            self._quantity = 5

    def concatenate(self, text, item):
        text += NEWS_TEXT.format(item['title'],
                                 item['url'],
                                 item['score'])
        return text

    def news_iterator(self, news_ids, text):
        for news_id in news_ids:
            item = self._client.get_item(news_id)
            text = self.concatenate(text, item)
        return text

class LatestNewsCommand(NewsCommand):
    name = '/latestnews'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = 'Latest {} Hacker News stories: \n\n'.format(self._quantity)
        news_ids = self._client.get_latest_items('newstories.json')[:self._quantity]
        text = self.news_iterator(news_ids, text)
        self.send_telegram_message(text)


class TopNewsCommand(NewsCommand):
    name = '/topnews'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = 'Top {} Hacker News stories: \n\n'.format(self._quantity)
        news_ids = self._client.get_latest_items('topstories.json')[:self._quantity]
        text = self.news_iterator(news_ids, text)
        self.send_telegram_message(text)

class BestNewsCommand(NewsCommand):
    name = '/bestnews'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = 'Best {} Hacker News stories: \n\n'.format(self._quantity)
        news_ids = self._client.get_latest_items('beststories.json')[:self._quantity]
        text = self.news_iterator(news_ids, text)
        self.send_telegram_message(text)
