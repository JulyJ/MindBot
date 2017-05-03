from pyowm import OWM, exceptions as owm_exceptions

from ..config import WEATHER_TOKEN
from ..commandbase import CommandBase


WEATHER_TEXT = ('City: {}\n'
                'Status: *{}*\n'
                'Temperature: *{}* Celsius\n'
                'Wind: *{} meter/sec*\n'
                'Humidity: *{}%*\n'
                'Atmospheric pressure: *{} hPa*')


class WeatherCommand(CommandBase):
    name = '/weather'
    owm_emoji_map = {
        '01d': '☀️',
        '01n': '☀️',
        '02d': '🌤',
        '02n': '🌤',
        '03d': '⛅️',
        '03n': '⛅️',
        '04d': '🌥',
        '04n': '🌥',
        '09d': '🌧',
        '09n': '🌧',
        '10d': '🌦',
        '10n': '🌦',
        '11d': '⛈',
        '11n': '⛈',
        '13d': '🌨',
        '13n': '🌨',
        '50d': '🌫',
        '50n': '🌫'
    }
    prefix = 'Current weather: \n\n'

    def get_emoji(self, weather):
        iconId = weather.get_weather_icon_name()
        if (self.owm_emoji_map[iconId]):
            return self.owm_emoji_map[iconId]

        return ''
    prefix = ' *Current weather:* \n\n'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            try:
                observation = OWM(WEATHER_TOKEN).weather_at_place(self._query)
            except owm_exceptions.OWMError:
                self.send_telegram_message('No such location 😭')
            else:
                weather = observation.get_weather()
                city = observation.get_location().get_name()
                status = weather.get_status()
                temperature = weather.get_temperature('celsius')
                wind = weather.get_wind()
                humidity = weather.get_humidity()
                pressure = weather.get_pressure()
                text = WEATHER_TEXT.format(city, status, temperature['temp'], wind['speed'], humidity, pressure['press'])
                self.prefix = self.get_emoji(weather) + ' ' + self.prefix
                return self.send_telegram_message(text=text)
        else:
            return self.send_telegram_message('Please pecify location')
