from requests import post
from urllib.parse import urlencode
from validators import url

from ..commandbase import CommandBase
from ..config import OCR_API_KEY

class OcrCommand(CommandBase):
    name = '/ocr'
    prefix = '🔍  *Text Parser:* \n'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if url(self._query):
            json = self.ocr_space_url(url=self._query)
            exit_code, error_message, text = self.parse_response(json)
            if exit_code == 1:
                self.send_telegram_message('`{}`'.format(text))
            else:
                self.send_telegram_message('*❗️ Error Message*: {}'.format(str(error_message)))
        else:
            self.send_telegram_message('No valid url provided.')

    def ocr_space_url(self, url, overlay=False, api_key=OCR_API_KEY, language='eng'):
        payload = {'url': url,
                   'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                  }
        response = post('https://api.ocr.space/parse/image',
                        data=payload,
                       )
        return response.json()

    def parse_response(self, json):
        print(json)
        text = ""
        exit_code = json['OCRExitCode']
        error_message = json['ErrorMessage']
        if exit_code == 1:
            for result in json['ParsedResults']:
                text += (result['ParsedText'])
        return exit_code, error_message, text
