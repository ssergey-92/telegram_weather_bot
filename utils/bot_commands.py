"""Module for setting telegram bot commands"""

from telebot import TeleBot
from telebot.types import BotCommand


from config_data.config import BOT_COMMANDS


def set_bot_commands(bot: TeleBot) -> None:
    """Set telegram bot commands."""

    bot_commands_list = []
    for i_command in BOT_COMMANDS:
        bot_commands_list.append(BotCommand(**i_command))
    bot.set_my_commands(bot_commands_list)
