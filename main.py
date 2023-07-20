import os
import requests
from aiogram import Bot, Dispatcher, executor, types

API_KEY = os.getenv("API_KEY")
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
bot = Bot(token=API_KEY)
dp = Dispatcher(bot=bot)


def get_currency_rate(base: str) -> float:
    """Получает курс от API и возвращает в виде float"""

    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.get(url, headers={"apikey": API_KEY_CURRENCY}, params={"base": base})
    rate = response.json()["rates"]["RUB"]
    return f'Курс {response.json()["base"]}/RUB - {rate}'


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("Узнать курс USD", callback_data=get_currency_rate("USD")))
    markup.add(types.InlineKeyboardButton("Узнать курс EUR", callback_data=get_currency_rate("EUR")))
    await message.answer("Выберите валюту!", reply_markup=markup)


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)


executor.start_polling(dp)
