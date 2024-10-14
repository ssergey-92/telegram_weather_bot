"""Module for catching callback query data with func=True and without state."""

from telebot.types import CallbackQuery

from .commands.city_weather import handle_city_wx_command
from bot_logger import app_logger
from config_data.config import CITY_WEATHER_COMMAND
from loader import bot


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery) -> None:
    """Catch unstated incoming callback query from inline keyboard.

    Call appropriate handling function according to bot commands.

    """
    app_logger.debug(f"Caught  command{call.data}")

    if call.data == CITY_WEATHER_COMMAND["command"]:
        handle_city_wx_command(call.from_user.id, call.message.chat.id)
