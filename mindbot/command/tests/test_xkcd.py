from json import loads
import requests_mock

from ..comics.xkcd import XkcdCommand
from mindbot.router import CommandRouter

instance = XkcdCommand(CommandRouter, '', {})
RESPONSE = '{"safe_title": "Doctor Visit", "img": "https://imgs.xkcd.com/comics/doctor_visit.png"}'


def test_json():
    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, text=RESPONSE)
        assert instance.get_json() == loads(RESPONSE)
