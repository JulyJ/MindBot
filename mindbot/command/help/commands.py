from ..commandbase import CommandBase

HELP_TEXT = ('Hi, {f[first_name]}  {f[last_name]}.\n'
             '/help - Show this message.\n'
             '/google - Trying to perform "feeling lucky" google search for the specified topic.\n'
             '/weather - Show current weather in the specified location.\n'
             '/wiki - Trying to search Wikipedia article for the specified topic.')

GREETINGS_TEXT = ('Greetings, {f[first_name]}  {f[last_name]}.\n\n'
                  'This is MindDumpBot. '
                  'He can google something for you or search in wikipedia. '
                  'Use "/help" command to see all functions.\n\n'
                  'Have a nice day!')


class GreetingsCommand(CommandBase):
    name = '/start'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = GREETINGS_TEXT.format(f=self._message['from'])
        self.send_telegram_message(text=text)


class HelpCommand(CommandBase):
    name = '/help'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = HELP_TEXT.format(f=self._message['from'])
        self.send_telegram_message(text=text)
