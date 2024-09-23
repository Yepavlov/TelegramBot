from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Menu"),
            KeyboardButton(text="About us"),
        ],
        [
            KeyboardButton(text="Shipping"),
            KeyboardButton(text="Payment"),
        ],

    ],
    resize_keyboard=True,
    input_field_placeholder="Input what would you like",
)

del_keyboard = ReplyKeyboardRemove()

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text="Menu"),
    KeyboardButton(text="About us"),
    KeyboardButton(text="Shipping"),
    KeyboardButton(text="Payment"),
)
start_kb2.adjust(2, 2)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(text="Leave a review"))

test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Create a poll", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text="Send your phone number 📱", request_contact=True),
            KeyboardButton(text="Send your location 🗺", request_location=True),
        ],
    ],
    resize_keyboard=True,

)
