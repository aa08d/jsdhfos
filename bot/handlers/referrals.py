from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from aiogram.utils.deep_linking import create_start_link

from bot.keyboards.start import main_menu_keyboard
from bot.filters.menu import MainMenuCallbackData
from bot.messages.referrals import INVITE_REFERRALS_TEXT, REFERRAL_START_TEXT
from marzban.client import MarzbanClient


router = Router()


@router.message(CommandStart(deep_link=True, deep_link_encoded=True, magic=F.args))
async def start_for_referrals_command(message: Message, command: CommandObject,  marzban: MarzbanClient) -> None:
    await message.answer(
        text=REFERRAL_START_TEXT.format(name=message.from_user.first_name),
        reply_markup=main_menu_keyboard,
    )
    user = await marzban.get_user(message.from_user.id)

    if user:
        return

    await marzban.add_user(message.from_user.id)
    await marzban.extend_subscription(int(command.args), 10)


@router.callback_query(MainMenuCallbackData.filter(F.category == "invite_friends"))
async def invite_friend_callback(callback: CallbackQuery) -> None:
    referral_link = await create_start_link(
        bot=callback.bot,
        payload=str(callback.from_user.id),
        encode=True,
    )
    await callback.message.answer(
        text=INVITE_REFERRALS_TEXT,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Скопировать",
                        copy_text=CopyTextButton(text=referral_link),
                    )
                ]
            ]
        )
    )
    await callback.answer()
