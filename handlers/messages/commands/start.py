"""Module for handling start command."""

from os import getenv as os_getenv, getenv
from traceback import format_exc
from telebot.types import Message

from loader import bot
from bot_logger import app_logger
from config_data.config import INTERNAL_ERROR_BOT_RESPONSE, START_COMMAND
from keyboards.inlines.options import options_inline_keyboard

welcome_msg = (
        "Welcome, {name}!\nI'm {bot_name}.\nI can find for your current "
        "weather in city."
)

@bot.message_handler(commands=[START_COMMAND["command"]])
def handle_start_command(message: Message) -> None:
    """Handle start command from user.

    Delete user state data if it is existed and send start message.

    """
    try:
        app_logger.info("Handling start command")
        bot.delete_state(message.from_user.id, message.chat.id)
        user_name = (
                message.from_user.first_name or
                message.from_user.full_name or
                message.from_user.username
        )
        bot.send_message(
            message.chat.id,
            welcome_msg.format(name=user_name, bot_name=os_getenv("BOT_NAME")),
            reply_markup=options_inline_keyboard,
        )
    except Exception as exc:
        app_logger.error(format_exc())
        bot.send_message(message.chat.id, INTERNAL_ERROR_BOT_RESPONSE)
