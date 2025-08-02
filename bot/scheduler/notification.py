from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.filters.menu import MainMenuCallbackData
from marzban.client import MarzbanClient


NOTIFICATION_TEXT = """
Привет! 👋
У тебя осталось всего 3 дня с твоей подпиской. Не забудь продлить её, чтобы и дальше пользоваться нашим сервисом!
"""


def is_three_days_apart(expire_date: int) -> None:
    if expire_date == 0 or expire_date is None:
        return

    different = datetime.fromtimestamp(expire_date) - datetime.now()
    return timedelta(days=2) < different < timedelta(days=3)


async def notify_users_sub_is_end(bot: Bot, marzban: MarzbanClient) -> None:
    users = await marzban.get_users()

    for user in users:
        if "_" not in user.username:
            continue

        telegram_id = user.username.split("_")[1]

        if not is_three_days_apart(user.expire):
            continue

        await bot.send_message(
            chat_id=telegram_id,
            text=NOTIFICATION_TEXT,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="💳 Пополнить",
                            callback_data=MainMenuCallbackData(category="payment").pack(),
                        ),
                    ],
                ],
            ),
        )
