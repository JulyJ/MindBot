from pyowm import OWM, exceptions as owm_exceptions

from ..config import WEATHER_TOKEN
from ..commandbase import CommandBase


FORECAST_TEXT = ('*Forecast time: {}*\n\n'
                 'City: {}\n'
                 'Status: *{}*\n'
                 'Day temperature: *{}* Celsius\n'
                 'Night temperature: *{}* Celsius\n'
                 'Wind: {} meter/sec')


class ForecastCommand(CommandBase):
    name = '/forecast'
    prefix = '🌤  *3-days forecast:* \n'

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self._query:
            try:
                forecast = OWM(WEATHER_TOKEN).daily_forecast(self._query, limit=3)
            except owm_exceptions.OWMError:
                self.send_telegram_message('No such location 😭')
            else:
                weathers = forecast.get_forecast()
                for weather in weathers.get_weathers():
                    city = weathers.get_location().get_name()
                    date = weather.get_reference_time('iso')
                    status = weather.get_status()
                    temperature = weather.get_temperature('celsius')
                    wind = weather.get_wind()
                    text = FORECAST_TEXT.format(date, city, status, temperature['day'], temperature['night'], wind['speed'])
                    self.send_telegram_message(text=text)
        else:
            return self.send_telegram_message('Please pecify location')
