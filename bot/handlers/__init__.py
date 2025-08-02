from aiogram import Dispatcher

from .referrals import router as referrals_router
from .payment import router as payment_router
from .connect import router as connect_router
from .start import router as start_router


def include_routers(dp: Dispatcher) -> None:
    dp.include_router(referrals_router)
    dp.include_router(payment_router)
    dp.include_router(connect_router)
    dp.include_router(start_router)
