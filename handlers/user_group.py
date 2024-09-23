from string import punctuation

from aiogram.filters import CommandStart, Command
from aiogram import types, Router

from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup", ]))

restricted_words = {"fuck", "bitch", "loser", "war"}


def clean_text(text: str) -> str:
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message) -> None:
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.username}, follow the rules of this chat!")
        await message.delete()
        # await message.chat.ban(message.from_user.id)                       !!! this code allows you to ban the user
