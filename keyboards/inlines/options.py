"""Module for creating inline keyboard with bot options."""

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from config_data.config import CITY_WEATHER_COMMAND

def get_options_inline_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard telegram bot options commands."""

    options_keyboard = InlineKeyboardMarkup(row_width=2)
    options_keyboard.add(
        InlineKeyboardButton(
            text=CITY_WEATHER_COMMAND["description"],
            callback_data=CITY_WEATHER_COMMAND["command"],
        )
    )
    return options_keyboard


options_inline_keyboard = get_options_inline_keyboard()
