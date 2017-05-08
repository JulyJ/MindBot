from requests import get

from ..commandbase import CommandBase

class HackerNewsClient():

    def get_latest_items(self,type):
        url = 'https://hacker-news.firebaseio.com/v0/{}'.format(type)
        response = get(url)
        return response.json()

    def get_item(self, item_id):
        url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(item_id)
        response = get(url).json()
        if 'url' in response:
            item = {'title': response['title'],
                    'url': response['url'],
                    'score': response['score']}
            return item

    def is_number(self, quantity):
        try:
            int(quantity)
            return True
        except ValueError:
            return False
