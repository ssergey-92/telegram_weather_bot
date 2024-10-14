"""Module with config data for telegram bot."""

from os import getenv as os_getenv
from sys import exit as sys_exit

from dotenv import load_dotenv, find_dotenv

START_COMMAND = {
    "command": "start",
    "description": "Start Weather Bot",
}
CANCEL_COMMAND = {
    "command": "cancel",
    "description": "Cansel searching weather forecast!",
}
CITY_WEATHER_COMMAND = {
    "command": "city_weather",
    "description": "Current weather in city",
}
BOT_COMMANDS = [START_COMMAND, CANCEL_COMMAND, CITY_WEATHER_COMMAND]
INTERNAL_ERROR_BOT_RESPONSE = (
    "Sorry bot is currently unavailable. Kindly try again latter!"
)

def load_env_data() -> None:
    """Load .env if bot is running without Docker."""

    if os_getenv("RUN_IN_DOCKER", "") == "True":
        pass
    elif not find_dotenv():
        sys_exit("File .env is not found.")
    else:
        load_dotenv()


load_env_data()