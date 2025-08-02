from datetime import datetime, timezone, timedelta

from marzban_api_client import AuthenticatedClient
from marzban_api_client.api.user import add_user, modify_user, get_user, get_users
from marzban_api_client.models import (
    UserCreate,
    UserModify,
    UserCreateProxies,
    UserCreateInbounds,
    UserResponse
)


proxies = UserCreateProxies.from_dict(
    {
        "vless": {
            "flow": "",
        },
    }
)

inbounds = UserCreateInbounds.from_dict(
    {
        "vless TCP": ["Steal", ],
    }
)


class MarzbanClient:
    def __init__(self, token: str, user: AuthenticatedClient) -> None:
        self._token = token
        self._user = user

    async def add_user(self, user_id: str) -> None:
        user = UserCreate(
            username=self.username(user_id),
            proxies=proxies,
            expire=int(self.expire()),
            inbounds=inbounds,
        )
        await add_user.asyncio(client=self._user, body=user)

    async def get_user(self, user_id: int) -> UserResponse:
        user = await get_user.asyncio(self.username(user_id), client=self._user)
        return user

    async def get_users(self) -> list[UserResponse]:
        users = await get_users.asyncio(client=self._user)
        return users.users

    async def extend_subscription(self, user_id: str, days: int) -> None:
        username = self.username(user_id)
        user = await get_user.asyncio(username, client=self._user)
        payload = UserModify(
            expire=int(self.extend_expire(user.expire, days))
        )
        await modify_user.asyncio(username, client=self._user, body=payload)

    async def get_user_subscription(self, user_id) -> str:
        user = await get_user.asyncio(
            username=self.username(user_id),
            client=self._user,
        )
        return user.subscription_url

    @staticmethod
    def username(tg_id: str) -> str:
        return f"user_{tg_id}"

    @staticmethod
    def expire() -> None:
        today = datetime.timestamp(datetime.now(tz=timezone(timedelta(hours=3))))
        return datetime.timestamp(
            datetime.fromtimestamp(today) + timedelta(days=10)
        )

    @staticmethod
    def extend_expire(expire_date: int, days: int) -> int:
        today = datetime.timestamp(datetime.now(tz=timezone(timedelta(hours=3))))

        if expire_date > today:
            return datetime.timestamp(
                datetime.fromtimestamp(expire_date) + timedelta(days=days)
            )

        return datetime.timestamp(
            datetime.fromtimestamp(today) + timedelta(days=days)
        )
