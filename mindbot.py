import json
import datetime
import urllib
import sqlite3
import requests
import re

import config

TOKEN = config.token
DBNAME = "minddump.db"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class MsgEcho:
    """This class accumulates all MindBot Methods. It needs to be decomposed."""

    database = None

    def get_url(self, url):
        """This method gets content (ex. JSON from /getUpdates telegram API method."""
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        """This method gets JSON dictionary from raw content"""
        content = self.get_url(url)
        dictionary = json.loads(content)
        return dictionary


    def get_updates(self, offset=None):
        """This method gets recent bot messages from API.
        Offset is optional parameter that helps us to ignore earlier messages """
        url = URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        dictionary = self.get_json_from_url(url)
        return dictionary


    def get_last_update_id(self, updates):
        """This method gets last message idto pass it to offset parameter."""
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def remember_all(self, updates):
        """This core method perform I/O jobs to DB, telegram, logs."""
        tags = ["", "", ""]
        print(tags[0], tags[1], tags[2])
        for update in updates["result"]:
            if 'message' not in update:
                continue
            if 'text' not in update["message"]:
                continue
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            date = update["message"]["date"]
            msg_tags = self.parse_tags(text)
            tag_counter = 0
            for tag in msg_tags:
                tags[tag_counter] = msg_tags[tag_counter]
                tag_counter += 1
            msg_from = update["message"]["from"]
            sender = msg_from["first_name"] + " " + msg_from["last_name"]
            self.log_message(text, chat, date)
            self.write_database(text, date, sender, tags[0], tags[1], tags[2])
            self.send_message(text, chat)

    def send_message(self, text, chat_id):
        """This method forms url to send message to telegram."""
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text="+"😎Remebered: \n\n"+"{}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    def log_message(self, text, chat_id, date):
        """This method log all messages to textfile."""
        log_string = "text: {}, chat_id: {}, date: {}".format(text, chat_id, self.date_conversion(date))
        text_file = open("log.txt", "a")
        print(log_string)
        text_file.write(log_string + "\n")
        text_file.close()

    def create_database(self):
        """This method initialize connection with DB"""
        conn = sqlite3.connect(DBNAME)
        print("Database created and opened succesfully")
        return conn

    def write_database(self, text, date, sender, tag1, tag2, tag3):
        """This method write messages to DB."""
        conn = self.create_database()
        cur = conn.cursor()
        text = text.replace("'", "`")               # Will be fixed soon.
        cur.execute("CREATE TABLE IF NOT EXISTS messages \
           (msg_text, msg_date, msg_sender, msg_tag1, msg_tag2, msg_tag3)")
        cur.execute("INSERT INTO messages VALUES ('{}', '{}', '{}','{}', '{}', '{}')" \
           .format(text, self.date_conversion(date), sender, tag1, tag2, tag3))
        conn.commit()
        conn.close()
        print("Message saved!")

    def date_conversion(self, date):
        date = datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')
        return date

    def read_database(self):
        """This method will search messages from DB in nearest future."""
        conn = self.create_database()
        # cur = conn.cursor()
        # cur.execute("")
        conn.commit()
        conn.close()

    def parse_tags(self, text):
        """This method find #tags in messages."""
        myre = re.compile(r"#[^\s]+")
        tags = myre.findall(text)
        return tags
