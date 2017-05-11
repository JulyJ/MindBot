from pyowm import OWM, exceptions as owm_exceptions

from mindbot.config import WEATHER_TOKEN
from ..commandbase import CommandBase

FORECAST_TEXT = ('*Forecast time: {fc_time}*\n\n'
                 'City: {city}\n'
                 'Status: *{status}*\n'
                 'Day temperature: *{temperature[day]}* Celsius\n'
                 'Night temperature: *{temperature[night]}* Celsius\n'
                 'Wind: {wind[speed]} meter/sec')


class ForecastCommand(CommandBase):
    name = '/forecast'
    help_text = '<LOCATION>- Show 3 days weather forecast in the specified location.'
    prefix = '🌤  *3-days forecast:* \n'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if not self._query:
            return self.send_telegram_message('Please pecify location')
        try:
            forecast = OWM(WEATHER_TOKEN).daily_forecast(self._query, limit=3)
        except owm_exceptions.OWMError:
            self.send_telegram_message('No such location 😭')
        else:
            weathers = forecast.get_forecast()
            for weather in weathers.get_weathers():
                text = FORECAST_TEXT.format(
                    fc_time=weather.get_reference_time('iso'),
                    city=weathers.get_location().get_name(),
                    status=weather.get_status(),
                    temperature=weather.get_temperature('celsius'),
                    wind=weather.get_wind(),
                )
                self.send_telegram_message(text=text)
