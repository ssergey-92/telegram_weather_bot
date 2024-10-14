from os import getenv as os_getenv
from typing import Optional

from requests.exceptions import JSONDecodeError, Timeout
from requests import get as request_get

from traceback import format_exc

from bot_logger import app_logger


class OpenWxMap:
    """Class OpenWxMap is used to take data from 'Open Weather Map'."""
    _base_url = "http://api.openweathermap.org/"
    _api_key = os_getenv("OPEN_WEATHER_MAP_KEY")
    _cities_coordinates_endpoint = "geo/1.0/direct"
    _current_wx_coordinates_endpoint = "data/2.5/weather"
    _possible_cities_limit = 10
    _request_timeout = 4
    _wx_units = "metric"
    _wx_report_lang = "en"


    @classmethod
    def get_possible_cities(cls, city_name: str) -> Optional[list]:
        """Get possible cities list with coordinates as per city name.

        Return cities list if response status code is 200 else None.

        """
        try:
            response = request_get(
                url=cls._base_url + cls._cities_coordinates_endpoint,
                params={
                    "q": city_name,
                    "limit": cls._possible_cities_limit,
                    "appid": cls._api_key,
                    },
                timeout=cls._request_timeout,
            )
            app_logger.info(f"{response.url=}, {response.status_code=}")
            if response.status_code == 200:
                return response.json()
            return
        except Timeout as exc:
            app_logger.error(format_exc())
            return
        except JSONDecodeError as exc:
            app_logger.error(format_exc())
            return

    @classmethod
    def get_wx_by_coordinates(cls, coordinates: dict) -> Optional[dict]:
        """Get current weather as per coordinates.

        Return current weather data if response status code is 200 else None.

        """
        try:
            response = request_get(
                url=cls._base_url + cls._current_wx_coordinates_endpoint,
                params={
                    "lat": coordinates["lat"],
                    "lon": coordinates["lon"],
                    "units": cls._wx_units,
                    "lang": cls._wx_report_lang,
                    "appid": cls._api_key,
                },
                timeout=cls._request_timeout,
            )
            app_logger.info(f"{response.url=}, {response.status_code=}")
            if response.status_code == 200:
                return response.json()
            return
        except Timeout as exc:
            app_logger.error(format_exc())
            return
        except JSONDecodeError as exc:
            app_logger.error(format_exc())
            return
