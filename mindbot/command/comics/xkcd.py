from requests import get

from ..commandbase import CommandBase

class XkcdCommand(CommandBase):
    name = '/xkcd'
    disable_web_page_preview = 'false'
    XKCD_TEXT = ('[{}]({})\n'
                 '*{}*\n'
                 '{}')

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            json = self.get_json(self._query)
        else:
            json = self.get_latest_json()
        if json:
            self.send_telegram_message(self.XKCD_TEXT.format(json['num'],
                                                             json['img'],
                                                             json['safe_title'],
                                                             json['alt']))
        else:
            self.send_telegram_message('No such xkcd strip.')

    def get_latest_json(self):
        url = 'https://xkcd.com/info.0.json'
        response = get(url)
        return response.json()

    def get_json(self, num):
        url = 'http://xkcd.com/{}/info.0.json'.format(num)
        response = get(url)
        if response.status_code == 200:
            return response.json()
