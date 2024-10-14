"""Module for saving state data."""

from typing import Any, Optional

from loader import bot


class BotStateStorage:

    @staticmethod
    def save_data(chat_id: int, user_id: int, data: dict) -> None:
        """Save data in bot state storage."""

        with bot.retrieve_data(user_id, chat_id) as state_data:
            for i_key, i_value in data.items():
                state_data[i_key] = i_value

    @staticmethod
    def get_user_data_by_key(
        chat_id: int, user_id: int, key: str,
    ) -> Optional[Any]:
        """Get user data by key from bot state storage."""

        with bot.retrieve_data(user_id, chat_id) as data:
            value = data.get(key)

        return value
