"""Module for handling start command."""

from os import getenv as os_getenv
from traceback import format_exc
from telebot.types import Message, User

from loader import bot
from bot_logger import app_logger
from config_data.config import INTERNAL_ERROR_BOT_RESPONSE, START_COMMAND
from keyboards.inlines.options import options_inline_keyboard

welcome_msg = (
        "Welcome, {name}!\nI'm {bot_name}.\nI can find for your current "
        "weather in city."
)


def handle_start_command(user: User, chat_id: int) -> None:
    """Handle 'start' command from user.

    Delete user state data if it is existed and send start message.

    """
    try:
        app_logger.info(f"Handling '{START_COMMAND["command"]}' Command")
        bot.delete_state(user.id, chat_id)
        user_name = user.first_name or user.full_name or user.username
        bot.send_message(
            chat_id,
            welcome_msg.format(name=user_name, bot_name=os_getenv("BOT_NAME")),
            reply_markup=options_inline_keyboard,
        )
    except Exception as exc:
        app_logger.error(format_exc())
        bot.send_message(chat_id, INTERNAL_ERROR_BOT_RESPONSE)


@bot.message_handler(commands=[START_COMMAND["command"]])
def get_start_command(message: Message) -> None:
    """Catch start command from user msg and call handling func."""

    handle_start_command(message.from_user, message.chat.id)
