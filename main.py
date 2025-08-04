import asyncio
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


from bot.handlers import include_routers
from marzban.config import MarzbanConfig
from marzban.client import MarzbanClient
from bot.scheduler.notification import notify_users_sub_is_end
from apscheduler.schedulers.asyncio import AsyncIOScheduler


TOKEN = "8040146816:AAF2v_Wk5NVd0vZ8iBvym7NGG2Ki6YpicSo"


async def init_marzban() -> MarzbanClient:
    config = MarzbanConfig(
        url="https://gadvpn.ru/",
        username="ophamino",
        password="Ad2685118",
    )

    return MarzbanClient(config=config)


async def main() -> None:
    marzban = await init_marzban()
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(
        bot=bot,
        marzban=marzban,
    )

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        notify_users_sub_is_end,
        trigger="interval",
        days=1,
        start_date=datetime.now() + timedelta(seconds=10),
        kwargs={"bot": bot, "marzban": marzban},
    )
    scheduler.start()

    include_routers(dp)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
