from aiogram.filters import CommandStart, Command
from aiogram import types, Router

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    await message.answer("It was a start command")


@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message) -> None:
    await message.answer("This is a menu:")


@user_private_router.message(Command("about"))
async def send_message_to_nika(message: types.Message) -> None:
    await message.answer("Information about our company:")

