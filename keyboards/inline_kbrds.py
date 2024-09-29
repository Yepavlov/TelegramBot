from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallBack(CallbackData, prefix="Menu"):
    level: int
    menu_name: str
    category: int | None = None
    page: int = 1
    product_id: int | None = None


def get_user_main_btns(*, level: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Assortment🍕🥤": "Catalog",
        "Cart🛒": "Cart",
        "About us❗": "About us",
        "Payment💲": "Payment",
        "Shipping🚕": "Shipping",
    }
    for text, menu_name in btns.items():
        if menu_name == "Catalog":
            keyboard.add(InlineKeyboardButton(text=text,
                                              callback_data=MenuCallBack(level=level + 1, menu_name=menu_name).pack()))
        elif menu_name == "Cart":
            keyboard.add(
                InlineKeyboardButton(text=text, callback_data=MenuCallBack(level=3, menu_name=menu_name).pack()))
        else:
            keyboard.add(
                InlineKeyboardButton(text=text, callback_data=MenuCallBack(level=level, menu_name=menu_name).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_user_catalog_btns(*, level: int, categories: list, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Back ⬅", callback_data=MenuCallBack(level=level - 1, menu_name="Menu").pack()))
    keyboard.add(InlineKeyboardButton(text="Cart 🛒", callback_data=MenuCallBack(level=3, menu_name="Cart").pack()))
    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                                          callback_data=MenuCallBack(level=level + 1,
                                                                     menu_name=category.name,
                                                                     category=category.id).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_product_btns(
        *,
        level: int,
        category: int,
        page: int,
        pagination_btns: dict,
        product_id: int,
        sizes: tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Back ⬅", callback_data=MenuCallBack(level=level - 1, menu_name="Catalog").pack()))
    keyboard.add(InlineKeyboardButton(text="Cart 🛒", callback_data=MenuCallBack(level=3, menu_name="Cart").pack()))
    keyboard.add(InlineKeyboardButton(text="Buy ✔", callback_data=MenuCallBack(level=level, menu_name="add_to_cart",
                                                                               product_id=product_id).pack()))
    keyboard.adjust(*sizes)
    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level=level,
                                                menu_name=menu_name,
                                                category=category,
                                                page=page + 1
                                            ).pack(), ))
        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level=level,
                                                menu_name=menu_name,
                                                category=category,
                                                page=page - 1
                                            ).pack(), ))
    return keyboard.row(*row).as_markup()


def get_user_cart(
        *,
        level: int,
        page: int | None,
        pagination_btns: dict | None,
        product_id: int | None,
        sizes: tuple[int] = (3,),
):
    keyboard = InlineKeyboardBuilder()
    if page:
        keyboard.add(InlineKeyboardButton(text="Delete",
                                          callback_data=MenuCallBack(level=level,
                                                                     menu_name="delete",
                                                                     product_id=product_id,
                                                                     page=page).pack()))
        keyboard.add(InlineKeyboardButton(text="-1",
                                          callback_data=MenuCallBack(level=level,
                                                                     menu_name="decrement",
                                                                     product_id=product_id,
                                                                     page=page).pack()))
        keyboard.add(InlineKeyboardButton(text="+1",
                                          callback_data=MenuCallBack(level=level,
                                                                     menu_name="increment",
                                                                     product_id=product_id,
                                                                     page=page).pack()))
        keyboard.adjust(*sizes)

        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == "next":
                row.append(InlineKeyboardButton(text=text,
                                                callback_data=MenuCallBack(level=level,
                                                                           menu_name=menu_name,
                                                                           page=page + 1).pack()))
            elif menu_name == "previous":
                row.append(InlineKeyboardButton(text=text,
                                                callback_data=MenuCallBack(level=level,
                                                                           menu_name=menu_name,
                                                                           page=page - 1).pack()))
        keyboard.row(*row)

        row2 = [
            InlineKeyboardButton(text="Home page 🏠", callback_data=MenuCallBack(level=0, menu_name="Menu").pack()),
            InlineKeyboardButton(text="Make order", callback_data=MenuCallBack(level=0, menu_name="Menu").pack()),
        ]
        return keyboard.row(*row2).as_markup()
    else:
        keyboard.add(InlineKeyboardButton(text="Home page 🏠", callback_data=MenuCallBack(level=0,
                                                                                         menu_name="Menu").pack()))
        return keyboard.adjust(*sizes).as_markup()


def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)
):
    keyboard = InlineKeyboardBuilder()
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()


def get_url_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,),
):
    keyboard = InlineKeyboardBuilder()
    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))
    return keyboard.adjust(*sizes).as_markup()


def get_inline_mix_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,),
):
    keyboard = InlineKeyboardBuilder()
    for text, value in btns.items():
        if "://" in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))
    return keyboard.adjust(*sizes).as_markup()
