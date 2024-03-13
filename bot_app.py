import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import time


load_dotenv()


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    url_addres = "http://127.0.0.1:8000/users/register/"
    registration_token = await generate_registration_token(user_id=user_id)
    registration_link = url_addres + registration_token
    await message.answer(
        f"Ссылка для регистрации: {registration_link}"
    )


async def generate_registration_token(user_id: int) -> str:
    token = f"registration_token_{user_id}?start_time={int(time.time())}&expiration_time={int(time.time()) + 60}"
    return token


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
