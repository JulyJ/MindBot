from logging import getLogger
from urllib.parse import urlencode

from requests import Response, get as http_get

from .config import telegram_url


class TelegramClient:
    def __init__(self, token: str):
        self.base_url = telegram_url.format(token)
        self._logger = getLogger(__name__)

    def get(self, url_name: str, get_params: dict=None) -> Response:
        get_params = get_params or {}
        get_params = {k: v for k, v in get_params.items() if v is not None}
        url = '{base}{method}{question}{query}'.format(
            base=self.base_url,
            method=url_name,
            question='?' if get_params else '',
            query=urlencode(get_params),
        )
        # self._logger.debug('Telegram API requested {url}'.format(url=url))
        return http_get(url)

    def get_text(self, url_name: str, get_params: dict=None):
        response = self.get(url_name, get_params)
        return response.content.decode()

    def get_json(self, url_name: str, get_params: dict=None):
        response = self.get(url_name, get_params)
        return response.json()
