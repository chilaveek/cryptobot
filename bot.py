from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import BOT_TOKEN
from pycoingecko import CoinGeckoAPI
from py_currency_converter import convert

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
cg = CoinGeckoAPI()

keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='💰Криптовалюты'),
            KeyboardButton(text='💸Конвертировать')
        ]
    ]

)


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}!", reply_markup=keyboard)


@dp.message_handler(text='💰Криптовалюты')
async def crypt(message: types.Message):
    price = cg.get_price(ids='bitcoin,ethereum,litecoin', vs_currencies='usd')
    await message.answer(
        text=
        f'💰Bitcoin: {price["bitcoin"]["usd"]:.2f}$\n'
        f'💰Ethereum: {price["ethereum"]["usd"]:.2f}$\n'
        f'💰Litecoin: {price["litecoin"]["usd"]:.2f}$\n'
    )


@dp.message_handler(text='💸Конвертировать')
async def dollar(message: types.Message):
    conv = convert(amount=1, to=['RUB', 'EUR', 'UAH'])
    await message.answer(
        text=
        f'💸1 USD в RUB {conv["RUB"]}\n'
        f'💸1 USD в EUR {conv["EUR"]}\n'
        f'💸1 USD в UAH {conv["UAH"]}\n'
    )


if __name__ == '__main__':
    executor.start_polling(dp)
