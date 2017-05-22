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
        '_Copyright: {response[copyright]}_\n'
        '[HD URL]({response[hdurl]})'
    )

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        json = self.get_json()
        if json:
            self.send_telegram_message(self.APOD_TEXT.format(response=json))
        else:
            self.send_telegram_message('Error while processing the request.')

    def get_json(self):
        apod_url = 'https://api.nasa.gov/planetary/apod?'

        url = '{base}{query}'.format(
            base=apod_url,
            query=urlencode({'api_key': NASA_API_KEY}))
        try:
            response = get(url)
        except RequestException as e:
            self._logger.debug('RequestException {}'.format(e))
            return
        if response.status_code == status_codes.codes.ok:
            return response.json()
