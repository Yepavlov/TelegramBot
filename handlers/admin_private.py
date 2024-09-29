from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product, orm_get_products, orm_delete_product, orm_get_product, \
    orm_update_product, orm_get_categories, orm_get_info_pages, orm_change_banner_image
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.inline_kbrds import get_callback_btns
from keyboards.reply_kbrds import get_keyboard, del_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
    "Add product",
    "Assortment",
    "Add/change banner",
    placeholder="Choose an action",
)


class AddProduct(StatesGroup):
    name = State()
    description = State()
    category = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        "AddProduct:name": "Re-enter the product name",
        "AddProduct:description": "Re-enter the product description",
        "AddProduct:category": "Re-enter the product category",
        "AddProduct:price": "Re-enter the product price",
        "AddProduct:image": "This is the last step",
    }


@admin_router.message(Command("admin"))
async def admin_menu(message: types.Message) -> None:
    await message.answer("What would you like to do?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Assortment")
async def get_list_of_products(message: types.Message, session: AsyncSession) -> None:
    categories = await orm_get_categories(session)
    btns = {category.name: f"category_{category.id}" for category in categories}
    await message.answer("Choose the category:", reply_markup=get_callback_btns(btns=btns))


@admin_router.callback_query(F.data.startswith("category_"))
async def show_product(callback: types.CallbackQuery, session: AsyncSession):
    category_id = callback.data.split("_")[-1]
    for product in await orm_get_products(session, int(category_id)):
        await callback.message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}</strong>\n{product.description}\nThe price: {round(product.price, 2)}",
            reply_markup=get_callback_btns(btns={
                "Delete product": f"delete_{product.id}",
                "Change product": f"change_{product.id}",
            }),
        )
        await callback.answer()
        await callback.message.answer("Here is a list of products ⬆")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))
    await callback.answer("The product is deleted!")
    await callback.message.answer("The product is deleted!")


@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    product_for_change = await orm_get_product(session, int(product_id))
    AddProduct.product_for_change = product_for_change
    await callback.answer()
    await callback.message.answer("Enter the product name", reply_markup=del_keyboard)
    await state.set_state(AddProduct.name)


class AddBanner(StatesGroup):
    image = State()
    name = State()


@admin_router.message(StateFilter(None), F.text == "Add/change banner")
async def add_banner_image(message: types.Message, state: FSMContext):
    await message.answer("Upload the banner image", reply_markup=del_keyboard)
    await state.set_state(AddBanner.image)


@admin_router.message(AddBanner.image, F.photo)
async def upload_banner_image(message: types.Message, state: FSMContext, session: AsyncSession):
    banners = await orm_get_info_pages(session)
    btns = {banner.name: banner.name for banner in banners}
    await message.answer("Choose the banner image", reply_markup=get_callback_btns(btns=btns))
    await state.update_data(image=message.photo[-1].file_id)
    await state.set_state(AddBanner.name)


@admin_router.message(AddBanner.image)
async def upload_invalid_banner_image(message: types.Message):
    await message.answer("You entered invalid data, enter the banner image")


@admin_router.callback_query(AddBanner.name)
async def add_banner_name(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    if callback.data in [banner.name for banner in await orm_get_info_pages(session)]:
        await callback.answer()
        await state.update_data(name=callback.data)
    else:
        await callback.message.answer("Choose the banner name from the list")
        await callback.answer()
    data = await state.get_data()
    await orm_change_banner_image(session, data["name"], data["image"])
    await callback.message.answer("The banner image is added", reply_markup=ADMIN_KB)
    await state.clear()


# This code for FSM


@admin_router.message(StateFilter(None), F.text == "Add product")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Enter the name of product", reply_markup=del_keyboard)
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter("*"), Command("cancel"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
    await state.clear()
    await message.answer("Your action is canceled", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter("*"), Command("back"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "back")
async def cancel_handler(message: types.Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer("There is no the previous step, enter the name of the product or write 'cancel'")
        return
    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state and current_state == AddProduct.price:
            await state.set_state(previous)
            categories = await orm_get_categories(session)
            btns = {category.name: str(category.id) for category in categories}
            await message.answer(f"Ok, you turned back to the previous step \n {AddProduct.texts[previous.state]}",
                                 reply_markup=get_callback_btns(btns=btns))
            return
        elif step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ok, you turned back to the previous step \n {AddProduct.texts[previous.state]}")
            return
        previous = step


@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        if len(message.text) < 4 or len(message.text) > 150:
            await message.answer(
                "The product name should not be more than 150 characters\n and less than 4.\n Reenter the product name."
            )
            return
        await state.update_data(name=message.text)
    await message.answer("Enter the description of product")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def add_invalid_name(message: types.Message):
    await message.answer("You entered invalid data, enter the product name")


@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    categories = await orm_get_categories(session)
    btns = {category.name: str(category.id) for category in categories}
    await message.answer("Choose the product category", reply_markup=get_callback_btns(btns=btns))
    await state.set_state(AddProduct.category)


@admin_router.message(AddProduct.description)
async def add_invalid_description(message: types.Message):
    await message.answer("You entered invalid data, enter the product description")


@admin_router.callback_query(AddProduct.category)
async def add_category(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    if int(callback.data) in [category.id for category in await orm_get_categories(session)]:
        await callback.answer()
        await state.update_data(category=callback.data)
        await callback.message.answer("Enter the product price")
        await state.set_state(AddProduct.price)
    else:
        await callback.message.answer("Choose the category from the list")
        await callback.answer()


@admin_router.message(AddProduct.category)
async def add_invalid_category(message: types.Message):
    await message.answer("You entered invalid data, choose the category from the list")


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == "." and AddProduct.product_for_change:
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Enter valid data")
            return
        await state.update_data(price=message.text)
    await message.answer("Upload the image of the product")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.price)
async def add_invalid_price(message: types.Message):
    await message.answer("You entered invalid data, enter the product price")


@admin_router.message(AddProduct.image, or_f(F.photo, F.text == "."))
async def add_product_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == "." and AddProduct.product_for_change:
        await state.update_data(image=AddProduct.product_for_change.image)
    elif message.photo:
        await state.update_data(image=message.photo[-1].file_id)
    else:
        await message.answer("Upload the product image")
        return
    data = await state.get_data()
    try:
        if AddProduct.product_for_change:
            await orm_update_product(session=session, product_id=AddProduct.product_for_change.id, data=data)
            await message.answer("The product is changed", reply_markup=ADMIN_KB)
        else:
            await orm_add_product(session, data)
            await message.answer("The product is added", reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(f"Error: \n{str(e)}\n Contact the developer", reply_markup=ADMIN_KB)
        await state.clear()
    AddProduct.product_for_change = None


@admin_router.message(AddProduct.image)
async def add_invalid_product_image(message: types.Message):
    await message.answer("You entered invalid data, enter the product image")
