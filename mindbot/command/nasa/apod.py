"""
    This module provides methods to send user "A picture of the day".

    Powered by https://api.nasa.gov/
    Picture of the day will be send to user with standard telegram web page preview
    as well as picture description.

    API KEY is required. It is free after registration.
"""


from requests import get, status_codes, RequestException
from urllib.parse import urlencode

from mindbot.config import NASA_API_KEY
from ..commandbase import CommandBase


class APODCommand(CommandBase):
    name = '/apod'
    help_text = ' - Each day a different image or photograph of our fascinating universe.'
    disable_web_page_preview = 'false'
    APOD_TEXT = (
        '[{response[title]}]({response[url]})\n'
        '{response[explanation]}\n'
    )

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        json = self.get_json()
        if json:
            self.send_telegram_message(self.APOD_TEXT.format(response=json))
        else:
            self.send_telegram_message('Error while processing the request.')

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
        return 'https://api.nasa.gov/planetary/apod?{query}'.format(
            query=urlencode({'api_key': NASA_API_KEY})
        )
