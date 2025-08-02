from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.filters.menu import MainMenuCallbackData


main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="⚡ Подключиться",
            callback_data=MainMenuCallbackData(category="connect").pack(),
        ),
        InlineKeyboardButton(
            text="💳 Пополнить",
            callback_data=MainMenuCallbackData(category="payment").pack(),
        ),
    ],
    [
        InlineKeyboardButton(
            text="👥 Пригласить друзей",
            callback_data=MainMenuCallbackData(category="invite_friends").pack(),
        ),
    ],
    [
        InlineKeyboardButton(text="🛠 Поддержка", url="t.me/GadVpnSupport"),
    ],
])
