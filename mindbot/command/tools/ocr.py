"""
    This module parses text from images provided by URL.

    Powered by https://ocr.space/ this module provides user with
    text parsed from an image. The Image should be provided as URL in command
    message query.

    OCR_API_KEY is required fo this module. It is free after registration.

    Example:
        /ocr http://fabricjs.com/article_assets/2_7.png
"""

from typing import Tuple, Union

from requests import post
from validators import url as valid_url

from mindbot.config import OCR_API_KEY
from ..commandbase import CommandBase


class OcrCommand(CommandBase):
    name = '/ocr'
    help_text = '<LINK TO IMAGE> - Parses text from image.'
    prefix = '🔍  *Text Parser:* \n'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if valid_url(self._query):
            exit_code, error_message, text = self.parse_response()
            if exit_code == 1:
                self.send_telegram_message('`{}`'.format(text))
            else:
                self.send_telegram_message('*❗️ Error Message*: {e!s}'.format(e=error_message))
        else:
            self.send_telegram_message('No valid url provided.')

    def ocr_space_url(self):
        payload = {
            'url': self._query,
            'isOverlayRequired': False,
            'apikey': OCR_API_KEY,
            'language': 'eng',
        }
        response = post('https://api.ocr.space/parse/image', data=payload)
        return response.json()

    def parse_response(self) -> Tuple[int, str, Union[str, None]]:
        json = self.ocr_space_url()
        exit_code = json['OCRExitCode']
        error_message = json['ErrorMessage']
        if exit_code == 1:
            text = ''.join(result['ParsedText'] for result in json['ParsedResults'])
        else:
            text = None
        return exit_code, error_message, text
