from re import search as re_search
from typing import List

from ..commandbase import CalculateCommand
from .exchangerates import OpenExchangeRatesClient

class ExchangeCommand(CalculateCommand):
    name = '/exchange'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._exchange = OpenExchangeRatesClient()

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self.currency_parser(self._query):
            params = self._query.split(' ')
            rate = self._exchange.get_rate(params[1], params[2])
            if rate is not None:
                return self.send_telegram_message("*{}* {} = *{}* {}".format(
                    params[0],
                    params[1],
                    round(rate*float(params[0]), 2),
                    params[2]
                ))
            else:
                return self.send_telegram_message('Please specify existing currency')
        else:
                return self.send_telegram_message('Please specify query as ```<amount> <base currency> <target currency>```')

    def currency_parser(self, text) -> List[str]:
        return re_search(r'([0-9]+)\s([a-zA-Z]{3})\s([a-zA-Z]{3})', text)