"""Module contain states to get current wx in city."""

from telebot.handler_backends import State, StatesGroup

class CurrentCityWeather(StatesGroup):
    """
    Class CurrentCityWeather for getting current wx in city scenario.

    Attributes:
        input_city (State): input city name for wx forecast
        confirm_city (State): confirm city name from suggested list

    """
    input_city = State()
    confirm_city = State()
