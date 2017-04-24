from sqlite3 import connect as db_connect

from myparser import Parser

import config

DBNAME = config.dbname


class DataBaseConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self._connection = None

    def call(self, sql_query, params):
        if not self._connection:
            raise RuntimeError
        cursor = self._connection.cursor()
        cursor.execute(sql_query, params)
        self._connection.commit()

    def __enter__(self):
        self._connection = db_connect(DBNAME)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._connection.close()

    def write_database(self, text, date, sender, msg_tags):
        """This method write messages to DB."""
        print(msg_tags)
        self.call('CREATE TABLE IF NOT EXISTS messages (msg_text, msg_date, msg_sender, msg_tags)', ())
        self.call('INSERT INTO messages VALUES (?, ?, ?, ?)', (text, Parser.date_conversion(date), sender, msg_tags))
