from ..commandbase import CommandBase


GREETINGS_TEXT = (
    'Greetings, {f[first_name]}  {f[last_name]}.\n\n'
    'This is MindDumpBot. '
    'He can google something for you or search in wikipedia. '
    'Use "/help" command to see all functions.\n\n'
    'Have a nice day!'
)


class GreetingsCommand(CommandBase):
    name = '/start'
    help_text = None

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        text = GREETINGS_TEXT.format(f=self._message['from'])
        self.send_telegram_message(text=text)


class HelpCommand(CommandBase):
    name = '/help'
    help_text = 'Shows this message.'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        commands_help = ('{command} {help_text}'.format(
            command=command,
            help_text=help_text,
        ) for command, help_text in self._router.get_commands_help())
        text = 'Hi, {f[first_name]} {f[last_name]}.\n\n{commands_help}'.format(
            f=self._message['from'],
            commands_help='\n'.join(commands_help)
        )
        self.send_telegram_message(text=text)
