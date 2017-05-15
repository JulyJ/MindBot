from ..exchange.exchangerates import OpenExchangeRatesClient


client = OpenExchangeRatesClient()


def test_ok_currency():
    assert isinstance(client.get_rate('EUR', 'USD'), float)


def test_bad_base_currency():
    assert not client.get_rate('KAR', 'USD')


def test_bad_target_currency():
    assert not client.get_rate('EUR', 'KAR')


def test_bad_target_and_base_currency():
    assert not client.get_rate('KAR', 'KAR')


def test_empty_base_currency():
    assert not client.get_rate('', 'USD')


def test_empty_target_currency():
    assert not client.get_rate('EUR', '')


def test_empty_target_and_base_currency():
    assert not client.get_rate('', '')
