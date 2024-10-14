"""Module for catching unstated messages."""

from telebot.types import Message

from .commands.start import handle_start_command
from keyboards.inlines.options import options_inline_keyboard
from loader import bot
from bot_logger import app_logger

accepted_welcome_msg = ("hi", "hello")
unrecognised_reply_msg = (
    "'{msg}' is not recognised.\nSelect one of below options:"
)


@bot.message_handler()
def non_state_text_message(message: Message) -> None:
    """Catch unstated incoming user message.

    Compare message text with possible welcome message and send appropriate
    reply.

    """
    app_logger.debug(f"{message.text=}, {message.chat.id=}")
    if message.text.lower().strip() in accepted_welcome_msg:
        handle_start_command(message.from_user, message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            unrecognised_reply_msg.format(msg=message.text),
            reply_markup=options_inline_keyboard,
        )
