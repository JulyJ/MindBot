"""
    This module serves commands to retrieve Canadian News.

    Powered by http://www.statcan.gc.ca/, shows 4 actual news.
    Updated daily.
"""

from requests import get, RequestException, status_codes

from ..commandbase import CommandBase


class CanadaStatsCommand(CommandBase):
    name = '/canadastat'
    help_text = ' - Daily Articles with Open Canada Statistics reviews.'
    disable_web_page_preview = 'false'
    NEWS_TEXT = ('[{response[title]}](http://www.statcan.gc.ca{response[photo]})\n'
                 '{response[summary]}\n'
                 '{response[date]}, [Read More...](http://www.statcan.gc.ca{response[link]})')

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        json = self.get_json()
        if json:
            for article in json['daily']['article']:
                self.send_telegram_message(self.NEWS_TEXT.format(response=article))
        else:
            self.send_telegram_message('No news were retrieved.')

    def get_json(self):
        url = 'http://www.statcan.gc.ca/sites/json/daily-banner-eng.json'
        try:
            response = get(url)
        except RequestException as e:
            self._logger.debug('RequestException {}'.format(e))
            return
        if response.status_code == status_codes.codes.ok:
            return response.json()
