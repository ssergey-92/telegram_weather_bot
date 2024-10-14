from sys import exit as sys_exit

from telebot.custom_filters import StateFilter

from loader import bot
from bot_logger import app_logger
from utils.bot_commands import set_bot_commands
import handlers.messages


def load_telegram_bot() -> None:
    """Setting state filters, bot commands and launches telegram bot."""

    app_logger.info("Starting telegram bot")
    bot.add_custom_filter(StateFilter(bot))
    set_bot_commands(bot)
    bot.infinity_polling(skip_pending=True)


if __name__ == '__main__':
    load_telegram_bot()
else:
    sys_exit('Access is denied!')
