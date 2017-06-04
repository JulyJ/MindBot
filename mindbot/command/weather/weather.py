from pyowm import OWM, exceptions as owm_exceptions

from mindbot.config import WEATHER_TOKEN
from ..commandbase import CommandBase

WEATHER_TEXT = ('City: {city}\n'
                'Status: *{status}*\n'
                'Temperature: *{temperature[temp]}* Celsius\n'
                'Wind: *{wind[speed]} meter/sec*\n'
                'Humidity: *{humidity}%*\n'
                'Atmospheric pressure: *{pressure[press]} hPa*')


class WeatherCommand(CommandBase):
    name = '/weather'
    help_text = '<LOCATION>- Show current weather in the specified location.'
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
    prefix = ' *Current weather:* \n\n'

    @classmethod
    def get_emoji(cls, weather):
        icon_id = weather.get_weather_icon_name()
        if cls.owm_emoji_map[icon_id]:
            return cls.owm_emoji_map[icon_id]
        return ''

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            try:
                observation = OWM(WEATHER_TOKEN).weather_at_place(self._query)
            except owm_exceptions.OWMError:
                self.send_telegram_message('No such location 😭')
            else:
                weather = observation.get_weather()
                text = WEATHER_TEXT.format(
                    city=observation.get_location().get_name(),
                    status=weather.get_status(),
                    temperature=weather.get_temperature('celsius'),
                    wind=weather.get_wind(),
                    humidity=weather.get_humidity(),
                    pressure=weather.get_pressure(),
                )
                self.prefix = self.get_emoji(weather) + ' ' + self.prefix
                return self.send_telegram_message(text=text)
        else:
            return self.send_telegram_message('Please specify location')
