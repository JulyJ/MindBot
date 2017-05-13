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
        with self._database as db:
            db.add_message(
                text=self._message['text'],
                date=self.date,
                sender=self.sender,
                tags=parse_tags(self._message['text']),
            )
        self.send_telegram_message(self._message['text'])

    @property
    def sender(self):
        return '{0[first_name]}'.format(self._message['from'])

    @property
    def date(self) -> datetime:
        """This method convert unixtime date to human-readable format"""
        timestamp = int(self._message['date'])
        return datetime.fromtimestamp(timestamp)
