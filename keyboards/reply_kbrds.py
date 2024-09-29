from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),

):
    """
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
        "Menu",
        "About our store",
        "Payment",
        "Shipping",
        "Send my phone number",
        placeholder="Input what would you like",
        request_contact=4,
        sizes(2, 2, 1)
    )
    """
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)


del_keyboard = ReplyKeyboardRemove()

# Creation keyboards examples.

# start_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Menu"),
#             KeyboardButton(text="About us"),
#         ],
#         [
#             KeyboardButton(text="Shipping"),
#             KeyboardButton(text="Payment"),
#         ],
#
#     ],
#     resize_keyboard=True,
#     input_field_placeholder="Input what would you like",
# )
#
# start_kb2 = ReplyKeyboardBuilder()
# start_kb2.add(
#     KeyboardButton(text="Menu"),
#     KeyboardButton(text="About us"),
#     KeyboardButton(text="Shipping"),
#     KeyboardButton(text="Payment"),
# )
# start_kb2.adjust(2, 2)
#
# start_kb3 = ReplyKeyboardBuilder()
# start_kb3.attach(start_kb2)
# start_kb3.row(KeyboardButton(text="Leave a review"))
#
# test_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Create a poll", request_poll=KeyboardButtonPollType()),
#         ],
#         [
#             KeyboardButton(text="Send your phone number 📱", request_contact=True),
#             KeyboardButton(text="Send your location 🗺", request_location=True),
#         ],
#     ],
#     resize_keyboard=True,
#
# )
