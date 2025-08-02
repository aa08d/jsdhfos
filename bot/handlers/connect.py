from aiogram import Router, F

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from bot.filters.menu import MainMenuCallbackData
from marzban.client import MarzbanClient


router = Router()


class OSChoiceCallback(CallbackData, prefix="connect"):
    os: str


@router.callback_query(MainMenuCallbackData.filter(F.category == "connect"))
async def connect_callback(callback: CallbackQuery) -> None:
    await callback.message.answer(
        text="Выберите свое устройство",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🤖 Android",
                        callback_data=OSChoiceCallback(os="android").pack(),
                    ),
                    InlineKeyboardButton(
                        text="🍎 iOS",
                        callback_data=OSChoiceCallback(os="ios").pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🖥️  Windows",
                        callback_data=OSChoiceCallback(os="windows").pack(),
                    ),
                    InlineKeyboardButton(
                        text="💻 MacOS",
                        callback_data=OSChoiceCallback(os="mac_os").pack(),
                    ),
                ],
            ],
        ),
    )


download_links = {
    "android": "https://play.google.com/store/apps/details?id=com.v2raytun.android",
    "ios": "https://apps.apple.com/en/app/v2raytun/id6476628951",
    "windows": "https://storage.v2raytun.com/v2RayTun_Setup.exe",
    "mac_os": "https://apps.apple.com/en/app/v2raytun/id6476628951",
}
deeplink_template = "https://gadvpn-preview.ru/?target={subscription_url}"
MANUAL_TEXT = """
1. 📥 <b>Скачайте приложение</b> <code>v2rantun</code> на ваше устройство.
2. 💡 <b>Нажмите кнопку "<i>Добавить ключ</i>"</b> в приложении.
3. 🔵 <b>Нажмите синюю кнопку</b> для продолжения.

<b>Готово! 🎉 Теперь вы подключены!</b>

"""


@router.callback_query(OSChoiceCallback.filter())
async def os_choice_callback(
    callback: CallbackQuery,
    callback_data: OSChoiceCallback,
    marzban: MarzbanClient,
) -> None:
    user_subscription = await marzban.get_user_subscription(callback.from_user.id)
    download_link = download_links[callback_data.os]
    deeplink = deeplink_template.format(subscription_url=user_subscription)

    await callback.message.answer(
        text=MANUAL_TEXT,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📥 Скачать приложение", url=download_link),
                ],
                [
                    InlineKeyboardButton(text="🔑 Добавить ключ", url=deeplink),
                ],
            ],
        ),
    )
