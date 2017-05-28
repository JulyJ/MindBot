from json import dumps
import requests_mock
from unittest.mock import MagicMock

from mindbot.command.tools.ocr import OcrCommand
from mindbot.router import CommandRouter
from .fixtures import fake_ocr_response, fake_ocr_error_response

instance = OcrCommand(CommandRouter, "http://test.ru", {})


def test_ocr_space_url():
    with requests_mock.mock() as m:
        m.post('https://api.ocr.space/parse/image',
               text=dumps(fake_ocr_response()))
        assert instance.ocr_space_url() == fake_ocr_response()


def test_parse_response():
    instance.ocr_space_url = MagicMock(return_value=fake_ocr_response())
    assert instance.parse_response() == (1, 'null', 'This is a sample parsed result')


def test_parse_error_response():
    instance.ocr_space_url = MagicMock(return_value=fake_ocr_error_response())
    assert instance.parse_response() == (2, 'null', None)


def test_call_ok():
    instance.parse_response = MagicMock(return_value=(1, 'null', 'Parsed result'))
    instance.send_telegram_message = MagicMock()
    instance()
    instance.send_telegram_message.assert_called_with('`Parsed result`')


def test_call_no_valid_url():
    instance = OcrCommand(CommandRouter, "parrot", {})
    instance.parse_response = MagicMock(return_value=(1, 'null', 'Parsed result'))
    instance.send_telegram_message = MagicMock()
    instance()
    instance.send_telegram_message.assert_called_with('No valid url provided.')


def test_call_parse_error():
    instance.parse_response = MagicMock(return_value=(2, 'null', None))
    instance.send_telegram_message = MagicMock()
    instance()
    instance.send_telegram_message.assert_called_with('*❗️ Error Message*: null')
