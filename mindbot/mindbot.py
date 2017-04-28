from logging import getLogger
from operator import itemgetter
from time import sleep

from .commands import CommandRouter
from .config import poll_interval, TELEGRAM_TOKEN
from .telegram import TelegramClient


class MindBot:
    router = CommandRouter

    def __init__(self):
        self._telegram = TelegramClient(token=TELEGRAM_TOKEN)
        self._last_update_id = None
        self._poll_interval = poll_interval
        self._logger = getLogger(__name__)

    def get_updates(self):
        updates = self._telegram.get_json(
            url_name='getUpdates',
            get_params={'offset': self._last_update_id},
        )
        msg = 'Updates fetched with offset {}'.format(self._last_update_id)
        self._logger.debug(msg)
        return updates['result']


    def set_last_update_id(self, updates):
        update_ids = map(itemgetter('update_id'), updates)
        self._last_update_id = max(map(int, update_ids)) + 1

    @staticmethod
    def route_message(updates):
        messages = (
            update['message'] for update in updates
            if 'text' in update.get('message', {})
        )
        for message in messages:
            CommandRouter.route(message)

    def run(self):
        self._logger.debug('MindBot started')
        try:
            while True:
                updates = self.get_updates()
                if updates:
                    self._logger.debug('Update received')
                    self.set_last_update_id(updates)
                    self.route_message(updates)
                sleep(self._poll_interval)
        except KeyboardInterrupt:
            return


if __name__ == '__main__':
    mind_bot = MindBot()
    mind_bot.run()
