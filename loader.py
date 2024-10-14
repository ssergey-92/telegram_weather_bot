"""Module to init telegram bot, state storage, load .env and handlers.

Package import sequence is important.
"""

from os import getenv

from telebot import TeleBot, storage

from config_data.config import load_env_data

load_env_data()
state_storage = storage.StateMemoryStorage()
bot = TeleBot(token=getenv("BOT_TOKEN"), state_storage=state_storage)
