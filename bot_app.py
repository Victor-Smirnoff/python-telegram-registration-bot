import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from token_service import generate_jwt_registration_token


load_dotenv()

HTTP_API_TELEGRAM_TOKEN = os.getenv("HTTP_API_TELEGRAM_TOKEN")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


bot = Bot(token=HTTP_API_TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    url_addres_for_register = "http://127.0.0.1:8000/users/register/"
    registration_token = await generate_jwt_registration_token(
        user_id=user_id,
        jwt_secret_key=JWT_SECRET_KEY
    )

    registration_link = url_addres_for_register + registration_token
    await message.answer(
        f"Ссылка для регистрации: {registration_link}"
    )


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
