import json
from requests import get
from urllib.parse import urlencode

from ..commandbase import SearchCommand


class UrbanDictionaryCommand(SearchCommand):
    name = '/urban'
    URBAN_TEXT = (
        '*Definition:* {}\n'
        '*Link*: {}\n'
        '👍 {} '
        '👎 {}'
    )

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            definitions = self.get_gefinition(self._query)['list']
            print(definitions)
            if definitions == []:
                return self.send_telegram_message('No definitions were found')
            for definition in definitions:
                self.send_telegram_message(self.URBAN_TEXT.format(
                    definition['definition'],
                    definition['permalink'],
                    definition['thumbs_up'],
                    definition['thumbs_down']))
        else:
            return self.send_telegram_message('Please specify query')

    def get_gefinition(self, query):
        urban_url = 'http://api.urbandictionary.com/v0/define?'

        url = '{base}{query}'.format(
            base=urban_url,
            query=urlencode({'term': query})
        )
        self._logger.debug('Urban Dictionary API requested {url}'.format(url=url))
        response = get(url).content.decode()
        return json.loads(response)

