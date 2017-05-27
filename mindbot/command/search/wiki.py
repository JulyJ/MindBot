"""
    This module serve commands to MediaWiki API.

    Powered by https://pypi.python.org/pypi/wikipedia/ it provides user
    with Wikipedia article search. WikiSearch class can perform Wikipedia
    search by specified query or return random Wikipedia article.

    Available commands:
        - /wiki
        - /random

    Example:
        /wiki parrot
"""

from wikipedia import exceptions as wiki_exceptions, page as wiki_page, random as wiki_random

from ..commandbase import SearchCommand


class WikiSearch(SearchCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.name == '/random':
            self._query = wiki_random()

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            try:
                page = wiki_page(self._query)
            except wiki_exceptions.PageError:
                self.send_telegram_message('No such page 😭')
            except wiki_exceptions.WikipediaException:
                self.send_telegram_message('Error while processing request 😭')
            else:
                content = page.content[:512]
                msg = '*{p.title}* \n\n{content}...\n\n[Read more at Wikipedia]({p.url})'
                self.send_telegram_message(msg.format(content=content, p=page))
        else:
            return self.send_telegram_message('Please specify query')


class WikiCommand(WikiSearch):
    name = '/wiki'
    help_text = '<QUERY> - Trying to search Wikipedia article for the specified topic.'


class RandomCommand(WikiSearch):
    name = '/random'
    help_text = ' - Gets a random Wikipedia article.'
