from string import punctuation

from aiogram.filters import Command
from aiogram import types, Router, Bot
from aiogram import F

from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup", ]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup", ]))

restricted_words = {"fuck", "bitch", "loser", "war"}


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    # pprint(admins_list)
    admins_list = [member.user.id for member in admins_list if
                   member.status == "administrator" or member.status == "creator"]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    # print(bot.my_admins_list)


def clean_text(text: str) -> str:
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message(F.text)
@user_group_router.message(F.text)
async def cleaner(message: types.Message) -> None:
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.username}, follow the rules of this chat!")
        await message.delete()
        # await message.chat.ban(message.from_user.id)                       !!! this code allows you to ban the user
