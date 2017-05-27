"""
    Simple QR generator, based on Google QR generator.

    This command class sends user URL that generates QR code. QR code  as image will be
    visible to the user by standard telegram web page preview.

    Example:
        /qr https://www.python.org/
"""

from urllib.parse import urlencode

from ..commandbase import CommandBase


class QrCommand(CommandBase):
    name = '/qr'
    help_text = '<QUERY> - Generate QR code.'
    disable_web_page_preview = 'false'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            self.send_telegram_message('[QR link]({0.form_url})'.format(self))
        else:
            self.send_telegram_message('No query provided.')

    @property
    def form_url(self):
        return 'https://chart.googleapis.com/chart?{query}'.format(
            query=urlencode({
                'cht': 'qr',
                'chs': '150x150',
                'chl': self._query,
            })
        )
