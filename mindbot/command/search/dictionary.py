from requests import get
import json
from urllib.parse import urlencode

from ..commandbase import SearchCommand
from ..config import DICTIONARY_APP_KEY, DICTIONARY_APP_ID


class DictionaryCommand(SearchCommand):
    name = '/oxford'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            json = self.get_json(self._query)
            if json:
                definitions = self.get_definitions(json)
                for definition in definitions:
                    self.send_telegram_message('*Definition:* {}\n'.format(definition))
            else:
                self.send_telegram_message('No definitions were found')
        else:
            self.send_telegram_message('Please specify query')

    def get_json(self, query):
        urban_url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'

        url = '{base}{language}/{query}'.format(
            base=urban_url,
            query=self._query.lower(),
            language='en'
        )
        self._logger.debug('Oxford Dictionary API requested {url}'.format(url=url))
        response = get(url, headers={'app_id': DICTIONARY_APP_ID,
                                     'app_key': DICTIONARY_APP_KEY})
        if response:
            return response.json()
        else:
            return None

    def get_definitions(self, json):
        definitions = []
        senses = self.get_senses(json)
        for sense in senses:
            definitions.append(sense['definitions'])
        return definitions

    def get_senses(self, definitions):
        senses = []
        entries = self.get_entries(definitions)
        for entry in entries:
            for sense in entry['senses']:
                senses.append(sense)
        return senses

    def get_entries(self, senses):
        entries = []
        lexical_entries = self.get_lexical_entries(senses)
        for lexical_entry in lexical_entries:
            for entry in lexical_entry['entries']:
                entries.append(entry)
        return entries

    def get_lexical_entries(self, entries):
        lexical_entries = []
        results = entries['results']
        for result in results:
            for lexical_entry in result['lexicalEntries']:
                lexical_entries.append(lexical_entry)
        return lexical_entries
