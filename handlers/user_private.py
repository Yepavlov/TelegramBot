from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F

from filters.chat_types import ChatTypeFilter
from keyboards.reply_kbrds import del_keyboard, test_kb

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private", ]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message) -> None:
    await message.answer("Hello, I'm a virtual assistant.", reply_markup=test_kb)


@user_private_router.message(or_f(Command("menu"), F.text.lower() == "menu"))
async def menu_cmd(message: types.Message) -> None:
    await message.answer("This is a menu:", reply_markup=del_keyboard)


@user_private_router.message(or_f(Command("about us"), F.text.lower() == "about us"))
async def about_cmd(message: types.Message) -> None:
    await message.answer("Information about our company:")


@user_private_router.message(or_f(Command("payment"), F.text.lower() == "payment"))
async def payment_cmd(message: types.Message) -> None:
    await message.answer("Payment information:")


@user_private_router.message(or_f(Command("shipping"), F.text.lower() == "shipping"))
async def shipping_cmd(message: types.Message) -> None:
    await message.answer("Shipping information:")


@user_private_router.message(F.contact)
async def get_contact(message: types.Message) -> None:
    await message.answer("The phone number was received", reply_markup=del_keyboard)
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_location(message: types.Message) -> None:
    await message.answer("Your location was received", reply_markup=del_keyboard)
    await message.answer(str(message.location))
