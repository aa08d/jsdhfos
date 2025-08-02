from aiogram.filters.callback_data import CallbackData


class MainMenuCallbackData(CallbackData, prefix="menu"):
    category: str
