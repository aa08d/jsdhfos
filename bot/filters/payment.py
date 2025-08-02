from aiogram.filters.callback_data import CallbackData


class PaymentDaysCallbackData(CallbackData, prefix="days"):
    days: str


class PaymentSucceededCallbackData(CallbackData, prefix="payment_succeeded"):
    payment_id: str
