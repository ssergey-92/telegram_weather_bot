"""Module for handling 'input_city' state of 'CurrentCityWeather'."""

from re import match as re_match
from traceback import format_exc
from typing import Optional

from telebot.types import Message

from bot_logger import app_logger
from config_data.config import INTERNAL_ERROR_BOT_RESPONSE
from handlers.sites_api.open_wx_map import OpenWxMap
from keyboards.inlines.cities import get_possible_cities_keyboard
from utils.bot_state_storage import BotStateStorage
from loader import bot
from states.current_city_weather import CurrentCityWeather

found_cities_msg = "Select one of the below options:"
msg_city_not_found = (
    "Sorry, there is no city '{city}' in our database.\n"
    "Try to enter proper city name or use another place."
)
uncorrect_city_name_error = (
    "Enter city name using ENGLISH letters and 1 space or hyphen if "
     "required!\n(ex. Moscow, Saint-Petersburg)"
)


def validate_city_name(city_name: str) -> Optional[str]:
    """ Check city name that match the format.

    Check that city name contains english letters and 1 space or hyphen in
    between.

    """

    pattern = r'^[A-Za-z]{2,}[\s\-]?[A-Za-z]{2,}$'
    city_name = re_match(pattern, city_name)
    if not city_name:
        return uncorrect_city_name_error



@bot.message_handler(state=CurrentCityWeather.input_city)
def handle_input_city_name(message: Message) -> None:
    """Handle user input city name.

    If user input city name is valid then get data from wx service and return
    corresponding msg to user.

    """
    try:
        clean_city_name = message.text.strip(" ,.")
        error_msg = validate_city_name(clean_city_name)
        if error_msg:
            bot.send_message(message.chat.id, error_msg)
            return

        possible_cities = OpenWxMap.get_possible_cities(clean_city_name)
        if not possible_cities:
            bot.send_message(
                message.chat.id, msg_city_not_found.format(city=message.text),
            )
            return

        BotStateStorage.save_data(
            message.chat.id,
            message.from_user.id,
            {"input_city": clean_city_name, "found_cities": possible_cities},
        )
        bot.set_state(message.from_user.id, CurrentCityWeather.confirm_city)
        bot.send_message(
            message.chat.id,
            found_cities_msg,
            reply_markup=get_possible_cities_keyboard(possible_cities),
        )
    except Exception as exc:
        app_logger.error(format_exc())
        bot.send_message(message.chat.id, INTERNAL_ERROR_BOT_RESPONSE)