import json
import urllib
import requests

import config


TOKEN = config.token

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class MsgEcho:
    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        dictionary = json.loads(content)
        return dictionary


    def get_updates(self, offset=None):
        url = URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        dictionary = self.get_json_from_url(url)
        return dictionary


    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)

    def echo_all(self, updates):
        for update in updates["result"]:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            self.send_message(text, chat)

    def remember_all(self, updates):
        for update in updates["result"]:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            self.remember_message(text, chat)

    def send_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text="+"😀Remebered: "+"{}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    def remember_message(self, text, chat_id):
        text_file = open("Output.txt", "w")
        print(text)
        text_file.write(text)
        text_file.close()


