from json import loads

from requests import get as http_get


class UrlGetter:
    "HTTP get and JSON PARSE"
    @staticmethod
    def get_url(url):
        """This method gets content (ex. JSON from /getUpdates telegram API method."""
        response = http_get(url)
        return response.content.decode()

    def get_json_from_url(self, url):
        """This method gets JSON dictionary from raw content"""
        content = self.get_url(url)
        return loads(content)
