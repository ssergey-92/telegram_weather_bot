"""Module to handle 'confirm_city' state of 'CurrentCityWeather' from callback."""

from json import loads as json_loads
from traceback import format_exc

from telebot.types import CallbackQuery

from bot_logger import app_logger
from config_data.config import INTERNAL_ERROR_BOT_RESPONSE
from handlers.sites_api.open_wx_map import OpenWxMap
from keyboards.inlines.options import options_inline_keyboard
from utils.bot_state_storage import BotStateStorage
from loader import bot
from states.current_city_weather import CurrentCityWeather

type_other_city_msg = "Type other city name:"


city_wx_report = (
    "Current weather in {city}:\n\n"
    "Temp: {temp}\n"
    "Humidity: {humidity}\n"
    "State: {state}\n\n"
    "Thank you for using our wx service!"
)
unavailable_wx_report = (
    "Currently weather for '{city} is not available!'\n"
    "Kindly select another location."
)


def get_wx_report_msg(city_data: dict, user_id: int, chat_id: int) -> str:
    """Create and return weather."""

    city_wx = OpenWxMap.get_wx_by_coordinates(city_data)
    app_logger.debug(city_wx)
    input_city = BotStateStorage.get_user_data_by_key(
        user_id, chat_id, "input_city",
    )
    if city_wx:
        state = "not available"
        temp = "not available"
        humidity = "not available"
        if (
                city_wx.get("weather") and
                city_wx.get("weather")[0].get("description")
        ):
            state = city_wx["weather"][0]["description"]
        if city_wx.get("main", {}).get("temp", ""):
            temp = "{temp}°c".format(temp=int(city_wx["main"]["temp"]))
        if city_wx.get("main", {}).get("humidity", ""):
            humidity = "{humidity}%".format(
                humidity=city_wx["main"]["humidity"],
            )
        return city_wx_report.format(
            city=input_city, temp=temp, humidity=humidity, state=state,
        )
    else:
        return unavailable_wx_report.format(city=input_city)


def handle_confirm_city_from_callback(call: CallbackQuery) -> None:
    """Handle 'confirm_city' state of 'CurrentCityWeather' from callback.

    If user select city from cities inline keyboard then return city weather if
    available.

    """
    try:
        cities_data = json_loads(call.data)
        if cities_data.get("other_city"):
            bot.set_state(call.from_user.id, CurrentCityWeather.input_city)
            bot.send_message(call.message.chat.id, type_other_city_msg)
        else:
            wx_report_msg = get_wx_report_msg(
                cities_data, call.from_user.id, call.message.chat.id,
            )
            bot.send_message(
                call.message.chat.id,
                wx_report_msg,
                reply_markup=options_inline_keyboard,
            )
            bot.delete_state(call.from_user.id, call.message.chat.id)

    except Exception as exc:
        app_logger.error(format_exc())
        bot.send_message(call.message.chat.id, INTERNAL_ERROR_BOT_RESPONSE)


@bot.callback_query_handler(
    func=lambda call: call, state=CurrentCityWeather.confirm_city,
)
def get_confirm_city_state_from_callback(call: CallbackQuery):
    """Catch state confirm_city from callback and call handling function."""

    app_logger.info(f"{call.from_user.id=}, {call.data=}")
    handle_confirm_city_from_callback(call)
