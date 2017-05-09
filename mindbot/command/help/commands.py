from ..commandbase import CommandBase

HELP_TEXT = ('Hi, {f[first_name]}  {f[last_name]}.\n\n'
             '`/help - Shows this message.\n'
             '/exchange <AMOUNT> <BASE CURRENCY> <TARGET CURRENCY> - Money exchange.\n'
             '/google <QUERY> - Trying to perform "feeling lucky" google search.\n'
             '/latestnews <N> - Gets N latest Hacker News stories.\n'
             '/topnews <N> - Gets N top Hacker News stories.\n'
             '/bestnews <N> - Gets N best Hacker News stories.\n'
             '/forecast <LOCATION>- Show 3 days weather forecast in the specified location.\n'
             '/weather <LOCATION>- Show current weather in the specified location.\n'
             '/wiki <QUERY> - Trying to search Wikipedia article for the specified topic.\n'
             '/urban <QUERY> - Looking for definitions in Urban Dictionary.\n'
             '/xkcd or /xkcd <number> - Latest or specific xkcd comics.\n'
             '/oxford <QUERY> - Looking for definitions in Oxford Dictionary.\n'
             '/qr <QUERY> - Generate QR code.\n'
             '/ocr <LINK TO IMAGE> - Parses text from image.\n'
             '/search <#TAG> - Searching database for messages with tags.\n'
             '/remember <text> <#TAG> - Write this message to the database.`'
            )

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
