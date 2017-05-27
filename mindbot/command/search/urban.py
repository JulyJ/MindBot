"""
    This module serves commands to Urban Dictionary API.

    Urban dictionary API is not officially announced, but valid
    and working fine. This module provides a user with Urban Dictionary
    definition search and returns all definitions and their ratings.

    Example:
        /urban parrot
"""

import json
from requests import get, status_codes, RequestException
from urllib.parse import urlencode

from ..commandbase import SearchCommand


class UrbanDictionaryCommand(SearchCommand):
    name = '/urban'
    help_text = '<QUERY> - Looking for definitions in Urban Dictionary.'
    URBAN_TEXT = (
        '*Definition:* {definition[definition]}\n'
        '*Link*: {definition[permalink]}\n'
        '👍 {definition[thumbs_up]} '
        '👎 {definition[thumbs_down]}'
    )

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            defs = self.get_definition()
            if not defs:
                return self.send_telegram_message('No definitions were found')
            else:
                [self.send_telegram_message(self.URBAN_TEXT.format(definition=d)) for d in defs]
        else:
            return self.send_telegram_message('Please specify query')

    def get_definition(self):
        urban_url = 'http://api.urbandictionary.com/v0/define?'

        url = '{base}{query}'.format(
            base=urban_url,
            query=urlencode({'term': self._query})
        )
        self._logger.debug('Urban Dictionary API requested {url}'.format(url=url))
        try:
            response = get(url)
        except RequestException as e:
            self._logger.debug('RequestException {}'.format(e))
            return
        if response.status_code == status_codes.codes.ok:
            return json.loads(response.content.decode())['list']
