import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')
DICTIONARY_APP_ID = os.environ.get('DICTIONARY_APP_ID')
DICTIONARY_APP_KEY = os.environ.get('DICTIONARY_APP_KEY')
OCR_API_KEY = os.environ.get('OCR_API_KEY')
NASA_API_KEY = os.environ.get('NASA_API_KEY')

poll_interval = 5
db_connection_string = 'sqlite:///minddump.db'
telegram_url = 'https://api.telegram.org/bot{}/'
exchangesrates_url = 'http://api.fixer.io/latest'
