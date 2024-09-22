import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv, find_dotenv

from common.bot_cmds_list import private
from handlers.user_private import user_private_router

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TELEGRAM_SECRET_KEY"))

dp = Dispatcher()

dp.include_router(user_private_router)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


asyncio.run(main())
