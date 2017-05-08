from requests import get
from urllib.parse import urlencode

from ..commandbase import CommandBase

class QrCommand(CommandBase):
    name = '/qr'
    disable_web_page_preview = 'false'


    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            self.send_telegram_message('[QR link]({})'.format(self.form_url(self._query)))
        else:
            self.send_telegram_message('No query provided.')

    def form_url(self, query):
        url = '{base}{query}'.format(
            base='https://chart.googleapis.com/chart?',
            query=urlencode({'cht': 'qr',
                             'chs': '150x150',
                             'chl': query}))
        return url
