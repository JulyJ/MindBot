from logging import getLogger
from urllib.parse import urlencode

from requests import get as http_get

from mindbot.config import exchangesrates_url


class OpenExchangeRatesClient:
    def __init__(self):
        self._logger = getLogger(__name__)

    def get_json(self, basecurrency):
        url = '{base}{question}{query}'.format(
            base=exchangesrates_url,
            question='?',
            query=urlencode({'base': basecurrency})
        )
        self._logger.debug('OpenExchangeRates API requested {url}'.format(url=url))
        return http_get(url).json()

    def get_rate(self, basecurrency, targetcurrency):
        rates = self.get_json(basecurrency)
        if 'error' in rates:
            return None
        else:
            return rates['rates'].get(targetcurrency)
