"""Module for handling city_weather command."""

from traceback import format_exc
from telebot.types import Message

from bot_logger import app_logger
from config_data.config import (
    CITY_WEATHER_COMMAND,
    INTERNAL_ERROR_BOT_RESPONSE,
)
from loader import bot
from states.current_city_weather import CurrentCityWeather

input_city_msg = "Input city name: "


def handle_city_wx_command(user_id: int, chat_id: int) -> None:
    """Handle city_weather command from user.

    Delete user state data if it is existed and init current_city_weather state.

    """
    try:
        app_logger.info(
            f"Handling '{CITY_WEATHER_COMMAND["command"]}' Command",
        )
        bot.delete_state(user_id, chat_id)
        bot.set_state(user_id, CurrentCityWeather.input_city)
        bot.send_message(chat_id, input_city_msg)
    except Exception as exc:
        app_logger.error(format_exc())
        bot.send_message(chat_id, INTERNAL_ERROR_BOT_RESPONSE)


@bot.message_handler(commands=[CITY_WEATHER_COMMAND["command"]])
def get_city_weather_command(message: Message) -> None:
    """Catch 'city_weather' command from user msg and call handling func."""

    handle_city_wx_command(message.from_user.id, message.chat.id)
