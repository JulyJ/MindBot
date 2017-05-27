"""
    This module implements google search for user by query.

    Example:
        /google parrot
"""

from urllib.parse import urlencode

from ..commandbase import SearchCommand


class GoogleCommand(SearchCommand):
    name = '/google'
    help_text = '<QUERY> - Trying to perform "feeling lucky" google search.'
    disable_web_page_preview = 'false'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            query = urlencode({'btnI': 'I', 'q': self._query})
            url = 'http://www.google.com/search?' + query
            return self.send_telegram_message(url)
        else:
            return self.send_telegram_message('Please specify query')
