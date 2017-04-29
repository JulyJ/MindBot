import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')

poll_interval = 5
db_connection_string = 'sqlite:///minddump.db'
telegram_url = 'https://api.telegram.org/bot{}/'
