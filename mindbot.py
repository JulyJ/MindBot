import json
import datetime
import urllib
import sqlite3
import re
import wikipedia
import requests


import config

TOKEN = config.token
GOOGLEKEY = config.google_api_key
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

    def remember_all(self, text, chat, date, msg_tags, sender):
        """This method performs I/O jobs to DB, telegram, logs."""
        print("remembering all...")
        tags = ["", "", ""]
        tag_counter = 0
        for tag in msg_tags:
            tags[tag_counter] = msg_tags[tag_counter]
            tag_counter += 1

        self.log_message(text, chat, date)
        self.write_database(text, date, sender, tags[0], tags[1], tags[2])
        self.send_remember_message(text, chat)

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
            msg_tags = self.parse_tags(text)
            msg_type = self.message_type_parser(text)
            msg_from = update["message"]["from"]
            sender = msg_from["first_name"] + " " + msg_from["last_name"]
            self.message_action(text, chat, date, msg_tags, sender, msg_type)

    def message_action(self, text, chat, date, msg_tags, sender, msg_type):
        """This method decides what action should bot perform based on first word"""
        print("message action...", msg_type)
        if msg_type == "google":
            self.google_search(text, chat)
        elif msg_type == "/start":
            self.send_greetings_message(sender, chat)
        elif msg_type == "wiki":
            self.wiki_search(text, chat)
        else:
            self.remember_all(text, chat, date, msg_tags, sender)

    def send_greetings_message(self, sender, chat_id):
        """This method sends greeting message."""
        print("sending greetings to telegram...")
        text = "Greetings, {}.\n\nThis is MindDumpBot. He can google something \
        for you or search in wikipedia. Use 'wiki <text>' or 'google <text>' \
        commands. Also it can remember all your messages, use #tags! \n\nHave a \
        nice day!".format(sender)
        print(text)
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    def send_remember_message(self, text, chat_id):
        """This method forms url to send message to telegram."""
        print("sending remember message to telegram...")
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text="+"😎Remebered: \n\n"+"{}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    def send_search_message(self, text, chat_id):
        """This method forms url to send message to telegram."""
        print("sending search message to telegram...")
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text="+"😎Find: \n\n"+"{}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    def log_message(self, text, chat_id, date):
        """This method log all messages to textfile."""
        date = self.date_conversion(date)
        log_string = "text: {}, chat_id: {}, date: {}".format(text, chat_id, date)
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
        """This method convert unixtime date to human-readable format"""
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
        print("parsed tags:", tags)
        return tags

    def google_search(self, text, chat):
        """This method performs Google search."""
        query = text.split(" ", 1)
        if len(query) > 1:
            url = "http://www.google.com/search?btnI=I&q={}".format(urllib.parse.quote(query[1]))
            print("google search: ", query[1])
            self.send_search_message(url, chat)

    def wiki_search(self, text, chat):
        """This method performs Wikipedia search."""
        query = text.split(" ", 1)
        if len(query) > 1:
            page = wikipedia.page(query[1])
            content = "{} {}".format(page.title, page.url)
            print("wiki search: ", query[1])
            print(page.title)
            self.send_search_message(content, chat)

    def message_type_parser(self, text):
        """This identifies user request (Remember information, Google, Wiki, translate etc."""
        print("message type parsing...")
        command = text.split(" ")[0]
        return command
