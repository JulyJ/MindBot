"""
    This module provides methods to send user information about closest o Earth asteroids.

    Powered by https://api.nasa.gov/
    User will receive information about 5 closest to Earth asteroids for the current day
    as well as links for this objects for further reading.

    API KEY is required. It is free after registration.
"""

from requests import get, status_codes, RequestException
from time import gmtime, strftime
from urllib.parse import urlencode

from mindbot.config import NASA_API_KEY
from ..commandbase import CommandBase


class AsteroidCommand(CommandBase):
    name = '/asteroids'
    help_text = " - Retrieve a list of 5 Asteroids based on today closest approach to Earth."
    today = strftime("%Y-%m-%d", gmtime())
    ASTEROID_TEXT = (
        'Name: [{object[name]}]({object[nasa_jpl_url]})\n'
        'Absolute Magnitude: {object[absolute_magnitude_h]}\n'
        'Minimum Diameter: {object[estimated_diameter][kilometers][estimated_diameter_min]}\n'
        'Maximum Diameter: {object[estimated_diameter][kilometers][estimated_diameter_max]}\n'
        'Hazardous? {object[is_potentially_hazardous_asteroid]}\n'
        )

    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        json = self.get_json()
        if json:
            objects = json['near_earth_objects'][self.today][:5]
            [self.send_telegram_message(self.ASTEROID_TEXT.format(object=o)) for o in objects]
        else:
            self.send_telegram_message('Error while processing the request.')

    def get_json(self):
        try:
            response = get(self.form_url)
        except RequestException as e:
            self._logger.debug('RequestException {}'.format(e))
            return
        if response.status_code == status_codes.codes.ok:
            return response.json()

    @property
    def form_url(self):
        return 'https://api.nasa.gov/neo/rest/v1/feed?{query}'.format(
            query=urlencode({'api_key': NASA_API_KEY,
                             'start_date': self.today,
                             'end_date': self.today})
        )
