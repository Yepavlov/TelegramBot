from aiogram.utils.formatting import as_marked_section, Bold, as_list

categories = ["Food", "Beverage", ]

description_for_info_pages = {
    "Menu": "Welcome to our store!",
    "About us": "Online store for selling pizza, \nWorking 24/7",
    "Payment": as_marked_section(
        Bold("Payment:"),
        "By card in bot",
        "By getting item in cash or by card",
        "In the store",
        marker="✔"
    ).as_html(),
    "Shipping": as_list(
        as_marked_section(
            Bold("Available delivery:"),
            "By courier",
            "Self-carriage",
            "I'll eat at your place",
            marker="✔"
        ),
        as_marked_section(
            Bold("Unavailable delivery:"),
            "By mail",
            "By pigeon",
            marker="❌"
        ),
        sep="\n--------------------------------\n"
    ).as_html(),
    "Catalog": "Category",
    "Cart": "Cart",
}
