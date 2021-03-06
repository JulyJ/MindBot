"""
    User can save any message to database. Better use #tags to search them later.

    Example:
        /remember Luck Is What Happens When Preparation Meets Opportunity #Seneca #luck
"""

from datetime import datetime

from mindbot.config import db_connection_string
from .db import DataBaseConnection
from .parser import parse_tags
from ..commandbase import CommandBase


class RememberAll(CommandBase):
    name = '/remember'
    help_text = '<text> <#TAG> - Write this message to the database.'
    prefix = '*😎Remebered:* \n\n'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._database = DataBaseConnection(db_connection_string)

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if not self._query:
            return self.send_telegram_message('Please specify message to remember.')
        with self._database as db:
            db.add_message(
                text=self._query,
                date=self.date,
                sender=self.sender,
                tags=parse_tags(self._query),
            )
        self.send_telegram_message(self._query)

    @property
    def sender(self):
        return '{0[first_name]}'.format(self._message['from'])

    @property
    def date(self) -> datetime:
        """This method convert unixtime date to human-readable format"""
        timestamp = int(self._message['date'])
        return datetime.fromtimestamp(timestamp)
