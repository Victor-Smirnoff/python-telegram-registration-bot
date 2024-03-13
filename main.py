import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv


load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Команда Старт")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
