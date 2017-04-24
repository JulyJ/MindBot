from urllib import parse

from wikipedia import exceptions as wiki_exceptions, page as wiki_page

import urlgetter
import config

TOKEN = config.token
URL = config.url.format(TOKEN)


class Searcher:
    def __init__(self):
        self._url_getter = urlgetter.UrlGetter()

    def send_search_message(self, text, chat_id):
        """This method forms url to send message to telegram."""
        print("sending search message to telegram...")
        text = parse.quote_plus(text)
        url = URL + "sendMessage?text="+"😎Found: \n\n"+"{}&chat_id={}".format(text, chat_id)
        self._url_getter.get_url(url)

    def google_search(self, text, chat):
        """This method performs Google search."""
        query = text.split(" ", 1)
        if len(query) > 1:
            url = "http://www.google.com/search?btnI=I&q={}".format(parse.quote(query[1]))
            print("google search: ", query[1])
            self.send_search_message(url, chat)

    def wiki_search(self, text, chat):
        """This method performs Wikipedia search."""
        query = text.split(" ", 1)
        if len(query) > 1:
            try:
                page = wiki_page(query[1])
                content = "{} {}".format(page.title, page.url)
                print("wiki search: ", query[1])
                print(page.title)
                self.send_search_message(content, chat)
            except wiki_exceptions.PageError:
                self.send_search_message("No such page 😭", chat)
            except wiki_exceptions.WikipediaException:
                self.send_search_message("Error while processing request 😭", chat)
