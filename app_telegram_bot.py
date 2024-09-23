import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from common.bot_cmds_list import private
from handlers.user_group import user_group_router
from handlers.user_private import user_private_router

ALLOWED_UPDATES = ["message", "edited_message", "callback_query", "inline_query", ]

bot = Bot(token=os.getenv("TELEGRAM_SECRET_KEY"))

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
