from urlgetter import UrlGetter
from msgsender import MsgSender
from myparser import Parser

import config

DBNAME = config.dbname
URL = config.url


class MsgListener:
    """This class accumulates core telegram-listening MindBot Methods."""

    database = None

    def __init__(self):
        self._url_getter = UrlGetter()
        self._parser = Parser()
        self._msg_sender = MsgSender()

    def get_updates(self, offset=None):
        """This method gets recent bot messages from API.
        Offset is optional parameter that helps us to ignore earlier messages """
        url = URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        return self._url_getter.get_json_from_url(url)

    def get_last_update_id(self, updates):
        """This method gets last message idto pass it to offset parameter."""
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def parse_message(self, updates):
        """This method parses telegram messages"""
        print("parsing message...")
        for update in updates["result"]:
            if 'message' not in update:
                continue
            if 'text' not in update["message"]:
                continue
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            date = update["message"]["date"]
            msg_tags = self._parser.parse_tags(text)
            msg_type = self._parser.message_type_parser(text)
            msg_from = update["message"]["from"]
            sender = msg_from["first_name"] + " " + msg_from["last_name"]
            self._msg_sender.message_action(text, chat, date, msg_tags, sender, msg_type)



