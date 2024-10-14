"""Module for creating cities inline keyboard"""

from json import dumps as json_dumps

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_full_city_name(city_data: dict) -> str:
    name = city_data.get("name", "")
    state = city_data.get("state", "")
    country = city_data.get("country", "")
    if not state or name == state:
        return f"{name}, {country}"

    return f"{name}, {state}, {country}"


def get_possible_cities_keyboard(
    found_cities: list[dict],
) -> InlineKeyboardMarkup:
    """Create inline keyboard with found cities names."""

    city_keyboard = InlineKeyboardMarkup(row_width=1)
    for i_city in found_cities:
        city_keyboard.add(
            InlineKeyboardButton(
                text=get_full_city_name(i_city),
                callback_data=json_dumps(
                    {"lat": i_city.get("lat", 0), "lon": i_city.get("lon", 0)},
                ),
            )
        )
    city_keyboard.add(
        InlineKeyboardButton(
            text="Type another city:",
            callback_data=json_dumps({"other_city": "other_city"}),
        )
    )
    return city_keyboard
