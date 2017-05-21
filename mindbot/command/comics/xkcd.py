from requests import get, status_codes, RequestException

from ..commandbase import CommandBase


class XkcdCommand(CommandBase):
    name = '/xkcd'
    help_text = '`[number]` - Latest or specific xkcd comics.'
    disable_web_page_preview = 'false'
    XKCD_TEXT = ('[{response[num]}]({response[img]})\n'
                 '*{response[safe_title]}*\n'
                 '{response[alt]}')

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        json = self.get_json()
        if json:
            self.send_telegram_message(self.XKCD_TEXT.format(response=json))
        else:
            self.send_telegram_message('No such xkcd strip.')

    def get_json(self):
        if self._query:
            url = 'http://xkcd.com/{}/info.0.json'.format(self._query)
        else:
            url = 'https://xkcd.com/info.0.json'
        try:
            response = get(url)
        except RequestException as e:
            self._logger.debug('RequestException {}'.format(e))
            return
        if response.status_code == status_codes.codes.ok:
            return response.json()
