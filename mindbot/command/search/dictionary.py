"""
    This module serves commands to Oxford Dictionary API.

    Oxford dictionary API documentation is available at official website
    https://developer.oxforddictionaries.com/. This module provides a user
    with Oxford Dictionary definition search and returns all definitions available.

    Registration for getting free API keys is required.

    Example:
        /oxford parrot
"""

from requests import get, status_codes

from mindbot.config import DICTIONARY_APP_ID, DICTIONARY_APP_KEY
from ..commandbase import SearchCommand


class DictionaryCommand(SearchCommand):
    name = '/oxford'
    help_text = '<QUERY> - Looking for definitions in Oxford Dictionary.'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            json = self.get_json()
            if json:
                definitions = self.get_definitions(json)
                for definition in definitions:
                    self.send_telegram_message('*Definition:* {}\n'.format(definition))
            else:
                self.send_telegram_message('No definitions were found')
        else:
            self.send_telegram_message('Please specify query')

    def get_json(self):
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/{query}'.format(
            query=self._query.lower())
        self._logger.debug('Oxford Dictionary API requested {url}'.format(url=url))
        response = get(url, headers={'app_id': DICTIONARY_APP_ID,
                                     'app_key': DICTIONARY_APP_KEY})
        if response.status_code == status_codes.codes.ok:
            return response.json()

    def get_definitions(self, json):
        definitions = []
        senses = self.get_senses(json)
        for sense in senses:
            if 'definitions' in sense:
                definitions.extend(sense['definitions'])
            else:
                continue
        return definitions

    def get_senses(self, json):
        senses = []
        entries = self.get_entries(json)
        for entry in entries:
            if 'senses' in entry:
                for sense in entry['senses']:
                    senses.append(sense)
            else:
                continue
        return senses

    def get_entries(self, json):
        entries = []
        lexical_entries = self.get_lexical_entries(json)
        for lexical_entry in lexical_entries:
            if 'entries' in lexical_entry:
                for entry in lexical_entry['entries']:
                    entries.append(entry)
            else:
                continue
        return entries

    def get_lexical_entries(self, json):
        lexical_entries = []
        results = json['results']
        for result in results:
            if 'lexicalEntries' in result:
                for lexical_entry in result['lexicalEntries']:
                    lexical_entries.append(lexical_entry)
            else:
                continue
        return lexical_entries
