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
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    await message.answer(
        f"Команда старт от пользователя “{user_first_name} {user_last_name}” "
        f"с айди “{user_id}” и айди чата “{chat_id}”"
    )


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
