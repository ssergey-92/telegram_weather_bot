"""Module to handle 'confirm_city' state of 'CurrentCityWeather' from msg."""

from traceback import format_exc

from telebot.types import Message

from bot_logger import app_logger
from config_data.config import INTERNAL_ERROR_BOT_RESPONSE
from keyboards.inlines.cities import get_possible_cities_keyboard
from utils.bot_state_storage import BotStateStorage
from loader import bot
from states.current_city_weather import CurrentCityWeather

select_city_notice = "Kindly select one of the below options to proceed:"


def handle_confirm_city_from_msg(message: Message) -> None:
    """Handle 'confirm_city' state of 'CurrentCityWeather' from msg.

    Return inline keyboard with found cities for selection.
    """
    try:
        possible_cities = BotStateStorage.get_user_data_by_key(
            message.from_user.id, message.chat.id, "found_cities"
        )
        bot.send_message(
            message.chat.id,
            select_city_notice,
            reply_markup=get_possible_cities_keyboard(possible_cities),
        )
    except Exception as exc:
        app_logger.error(format_exc())
        bot.send_message(message.chat.id, INTERNAL_ERROR_BOT_RESPONSE)


@bot.message_handler(state=CurrentCityWeather.confirm_city)
def get_confirm_city_state_from_msg(message: Message) -> None:
    """Catch state 'confirm_city' from message and call handling function."""

    app_logger.info(f"{message.from_user.id=}, {message.text=}")
    handle_confirm_city_from_msg(message)
