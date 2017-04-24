
from urllib import parse
from databaseconnection import DataBaseConnection
from urlgetter import UrlGetter
from searcher import Searcher
from myparser import Parser

import config

DBNAME = config.dbname
URL = config.url


class MsgSender:
    """This class accumulates core telegram-sending MindBot Methods."""

    database = None

    def __init__(self):
        self._database = DataBaseConnection(db_name=DBNAME)
        self._url_getter = UrlGetter()
        self._searcher = Searcher()


    def remember_all(self, text, chat, date, msg_tags, sender):
        """This method performs I/O jobs to DB, telegram, logs."""
        print("remembering all...")
        self.log_message(text, chat, date)
        with self._database as db:
            db.write_database(text, date, sender, msg_tags)
        self.send_remember_message(text, chat)

    def message_action(self, text, chat, date, msg_tags, sender, msg_type):
        """This method decides what action should bot perform based on first word"""
        print("message action...", msg_type)
        if msg_type == "google":
            self._searcher.google_search(text, chat)
        elif msg_type == "/start":
            self.send_greetings_message(sender, chat)
        elif msg_type == "wiki":
            self._searcher.wiki_search(text, chat)
        else:
            self.remember_all(text, chat, date, msg_tags, sender)

    def send_greetings_message(self, sender, chat_id):
        """This method sends greeting message."""
        print("sending greetings to telegram...")
        text = "Greetings, {}.\n\nThis is MindDumpBot. He can google something for you or search in wikipedia. Use 'wiki <text>' or 'google <text>' commands. Also it can remember all your messages, use #tags! \n\nHave a nice day!".format(sender)
        print(text)
        text = parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self._url_getter.get_url(url)

    def send_remember_message(self, text, chat_id):
        """This method forms url to send message to telegram."""
        print("sending remember message to telegram...")
        text = parse.quote_plus(text)
        url = URL + "sendMessage?text="+"😎Remebered: \n\n"+"{}&chat_id={}".format(text, chat_id)
        self._url_getter.get_url(url)

    @staticmethod
    def log_message(text, chat_id, date):
        """This method log all messages to textfile."""
        date = Parser.date_conversion(date)
        log_string = "text: {}, chat_id: {}, date: {}".format(text, chat_id, date)
        print(log_string)
        with open("log.txt", "a") as text_file:
            text_file.write(log_string + "\n")