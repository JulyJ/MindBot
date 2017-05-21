from json import dumps
import requests_mock
from unittest.mock import MagicMock

from mindbot.command.exchange.exchange import ExchangeCommand
from mindbot.command.exchange.exchangerates import OpenExchangeRatesClient
from mindbot.router import CommandRouter
from .fixtures import fake_exchange

exchange = ExchangeCommand(CommandRouter, '10 CAD EUR', {})
client = OpenExchangeRatesClient()


def test_get_json():
    with requests_mock.mock() as m:
        m.get('http://api.fixer.io/latest?base=CAD', text=dumps(fake_exchange()))
        assert client.get_json('CAD') == fake_exchange()


def test_get_existing_rate():
    client.get_json = MagicMock(return_value=fake_exchange())
    assert client.get_rate('CAD', 'EUR') == 0.65924


def test_get_not_existing_rate():
    client.get_json = MagicMock(return_value=fake_exchange())
    assert not client.get_rate('CAD', 'RUB')


def test_get_error_rate():
    client.get_json = MagicMock(return_value='{"error":"Invalid base"}')
    assert not client.get_rate('CAD', 'EUR')


def test_currency_parser_ok():
    assert exchange.currency_parser('10 CAD RUB')


def test_currency_parser_not_ok():
    assert not exchange.currency_parser('10 CAD in RUB')


def test_currency_parser_empty():
    assert not exchange.currency_parser('')


def test_call_parsed():
    exchange._exchange.get_rate = MagicMock(return_value=0.65924)
    exchange.send_telegram_message = MagicMock()
    exchange()
    exchange._exchange.get_rate.assert_called_with('CAD', 'EUR')
    exchange.send_telegram_message.assert_called_with('*10* CAD = *6.59* EUR')


def test_call_no_rate():
    exchange._exchange.get_rate = MagicMock(return_value=None)
    exchange.send_telegram_message = MagicMock()
    exchange()
    exchange.send_telegram_message.assert_called_with('Please specify existing currency')


def test_call_not_parsed():
    exchange_empty = ExchangeCommand(CommandRouter, '', {})
    exchange_empty.send_telegram_message = MagicMock()
    exchange_empty()
    msg = 'Please specify query as ```<amount> <base currency> <target currency>```'
    exchange_empty.send_telegram_message.assert_called_with(msg)
