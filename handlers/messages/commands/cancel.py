"""Module for handling cancel command."""

from traceback import format_exc
from telebot.types import Message

from loader import bot
from bot_logger import app_logger
from config_data.config import INTERNAL_ERROR_BOT_RESPONSE, CANCEL_COMMAND
from keyboards.inlines.options import options_inline_keyboard

cancel_msg = (
        "Your weather search state was canceled!"
        "\nSelect one of the below options:"
)


@bot.message_handler(commands=[CANCEL_COMMAND["command"]])
def handle_cancel_command(message: Message) -> None:
    """Handle cancel command from user.

    Delete user state data if it is existed and send cancel message.

    """
    try:
        app_logger.info(f"Handling '{CANCEL_COMMAND["command"]}' Command")
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(
            message.chat.id, cancel_msg, reply_markup=options_inline_keyboard,
        )
    except Exception as exc:
        app_logger.error(format_exc())
        bot.send_message(message.chat.id, INTERNAL_ERROR_BOT_RESPONSE)
