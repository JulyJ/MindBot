from ..commandbase import SearchCommand
from ..config import db_connection_string
from .db import DataBaseConnection
from .parser import parse_tags

class SearchTagCommand(SearchCommand):
    name = '/search'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._database = DataBaseConnection(db_connection_string)

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if not self._query:
            return self.send_telegram_message('Please pecify #tags')
        tags = parse_tags(self._message['text'])
        if not tags:
            return self.send_telegram_message('Please pecify #tags')
        with self._database as db:
            for tag in tags:
                messages = db.search_messages(tag)
                if not messages:
                    self.send_telegram_message('No records for {}'.format(tag))
                    continue
                for message in messages:
                    self.send_telegram_message(message)