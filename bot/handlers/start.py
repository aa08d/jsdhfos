from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.messages.start import NEW_USER_START_MESSAGE, OLD_USER_START_MESSAGE
from bot.keyboards.start import main_menu_keyboard
from marzban.client import MarzbanClient


router = Router()


@router.message(CommandStart())
async def start_command(message: Message, marzban: MarzbanClient) -> None:
    user = await marzban.get_user(message.from_user.id)

    if user is None:
        await message.answer(
            text=NEW_USER_START_MESSAGE.format(name=message.from_user.first_name),
            reply_markup=main_menu_keyboard,
        )
        await marzban.add_user(message.from_user.id)

        return

    await message.answer(
        text=OLD_USER_START_MESSAGE,
        reply_markup=main_menu_keyboard,
    )
