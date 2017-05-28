"""
    This module provides methods to send user photos form Curiosity rover.

    Powered by https://api.nasa.gov/

    User can specify number of photos he would like to receive, 3 by default.
    Date of photos is generated randomly starting from Curiosity landing in 2012
    and ending with current date.

    API KEY is required. It is free after registration.

    Example:
        /curiosity 10
"""

from radar import random_datetime
from requests import get, status_codes, RequestException
from time import gmtime, strftime
from urllib.parse import urlencode

from mindbot.config import NASA_API_KEY
from ..commandbase import CommandBase


class CuriosityCommand(CommandBase):
    name = '/curiosity'
    help_text = " - [N] Images gathered by NASA's Curiosity at a random day."
    disable_web_page_preview = 'false'
    CURIOSITY_TEXT = (
        '[{photo[earth_date]}]({photo[img_src]})\n'
        'Camera: {photo[camera][full_name]}'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._query.isdigit():
            self._quantity = int(self._query)
        else:
            self._quantity = 3

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        json = self.get_json()
        if json['photos']:
            photos = json['photos'][:self._quantity]
            [self.send_telegram_message(self.CURIOSITY_TEXT.format(photo=p)) for p in photos]
        else:
            self.send_telegram_message('No photos loaded yet. Try the previous day.')

    def get_json(self):
        try:
            response = get(self.form_url)
        except RequestException as e:
            self._logger.debug('RequestException {}'.format(e))
            return
        if response.status_code == status_codes.codes.ok:
            return response.json()

    @property
    def form_url(self):
        today = strftime("%Y-%m-%d", gmtime())
        date = random_datetime(start='2012-08-06', stop=today)  # 2012-08-06  - landing date
        return 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?{query}'.format(
            query=urlencode({'api_key': NASA_API_KEY,
                             'earth_date': date
                             })
        )
