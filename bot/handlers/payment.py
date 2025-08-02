import yookassa

from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.filters.menu import MainMenuCallbackData
from bot.filters.payment import PaymentDaysCallbackData, PaymentSucceededCallbackData
from marzban.client import MarzbanClient
from bot.payment.base import create


router = Router()


ONE_DAY_PRICE = 3.3


class PaymentState(StatesGroup):
    ON = State()


@router.callback_query(MainMenuCallbackData.filter(F.category == "payment"))
async def payment_callback(callback: CallbackQuery) -> None:
    await callback.message.answer(
        text="Выбериете необходимое количество дней",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                      text="30 дней",
                      callback_data=PaymentDaysCallbackData(days="30").pack(),
                    ),
                    InlineKeyboardButton(
                      text="90 дней",
                      callback_data=PaymentDaysCallbackData(days="90").pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="180 дней",
                        callback_data=PaymentDaysCallbackData(days="180").pack(),
                    ),
                    InlineKeyboardButton(
                        text="360 дней",
                        callback_data=PaymentDaysCallbackData(days="360").pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Другое количество дней",
                        callback_data=PaymentDaysCallbackData(days="other").pack(),
                    ),
                ],
            ],
        ),
    )


payment_invoice_text = """
<b>📅 Покупка подписки на {days} дней</b>
<b>Дата</b>: {date}

Для оплаты нажмите на кнопку <b>"💳 Оплатить"</b>.

После завершение оплаты нажмите кнопку <b>"✅ Я оплатил"</b>, чтобы мы могли проверить статус платежа и продлить подписку
"""


async def send_invoice(update: Message | CallbackQuery, days: int) -> None:
    payment_url, payment_id = create(days * ONE_DAY_PRICE, days)
    text = payment_invoice_text.format(
        days=days,
        date=datetime.now().date()
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💳 Оплатить", url=payment_url),
                InlineKeyboardButton(
                    text="✅ Я оплатил",
                    callback_data=PaymentSucceededCallbackData(payment_id=payment_id).pack(),
                ),
            ],
        ],
    )

    if isinstance(update, CallbackQuery):
        await update.message.answer(text, reply_markup=keyboard)
    if isinstance(update, Message):
        await update.answer(text, reply_markup=keyboard)


@router.callback_query(PaymentDaysCallbackData.filter(F.days == "other"))
async def select_days_payment_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Какое количество дней вы хотите?")
    await state.set_state(PaymentState.ON)
    await callback.answer()


@router.message(StateFilter(PaymentState.ON), F.text.regexp(r"^\d+$"))
async def other_days_payment_message(message: Message, state: FSMContext) -> None:
    await send_invoice(message, int(message.text))
    await state.clear()


@router.message(StateFilter(PaymentState.ON))
async def wrong_select_days_message(message: Message) -> None:
    await message.answer(
        "<b>Введите целое число.</b>\n\n <b>Например</b>: 100"
    )


@router.callback_query(PaymentDaysCallbackData.filter())
async def payment_days_callback(callback: CallbackQuery, callback_data: PaymentDaysCallbackData) -> None:
    await send_invoice(callback, int(callback_data.days))
    await callback.answer()


@router.callback_query(PaymentSucceededCallbackData.filter())
async def successful_payment_message(
    callback: CallbackQuery,
    callback_data: PaymentSucceededCallbackData,
    bot: Bot,
    marzban: MarzbanClient,
) -> None:
    payment = yookassa.Payment.find_one(callback_data.payment_id)

    if payment.status == "succeeded":
        days = payment.metadata["days"]

        await marzban.extend_subscription(callback.from_user.id, int(days))
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await callback.message.answer(f"🎉 <b>Оплата прошла успешно</b> 🎉\n\n✅ Продлили подпсику на {days} дней")

        return

    await callback.message.answer("<b>Оплата не прошла.</b>\n\n Если возникли трудности, обратитесь в поддержку")
