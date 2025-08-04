from datetime import datetime, timezone, timedelta

from marzban_api_client import Client, AuthenticatedClient
from marzban_api_client.api.user import add_user, modify_user, get_user, get_users
from marzban_api_client.models import (
    UserCreate,
    UserModify,
    UserCreateProxies,
    UserCreateInbounds,
    UserResponse
)
from marzban_api_client.models.body_admin_token_api_admin_token_post import BodyAdminTokenApiAdminTokenPost
from marzban_api_client.api.admin import admin_token

from .config import MarzbanConfig


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
    def __init__(self, config: MarzbanConfig) -> None:
        self._config = config

    async def add_user(self, user_id: str) -> None:
        client = await self.get_client()

        user = UserCreate(
            username=self.username(user_id),
            proxies=proxies,
            expire=int(self.expire()),
            inbounds=inbounds,
        )
        await add_user.asyncio(client=client, body=user)

    async def get_user(self, user_id: int) -> UserResponse:
        client = await self.get_client()
        user = await get_user.asyncio(self.username(user_id), client=client)
        return user

    async def get_users(self) -> list[UserResponse]:
        client = await self.get_client()
        users = await get_users.asyncio(client=client)
        return users.users

    async def extend_subscription(self, user_id: str, days: int) -> None:
        client = await self.get_client()
        username = self.username(user_id)
        user = await get_user.asyncio(username, client=client)
        payload = UserModify(
            expire=int(self.extend_expire(user.expire, days))
        )
        await modify_user.asyncio(username, client=client, body=payload)

    async def get_user_subscription(self, user_id) -> str:
        client = await self.get_client()
        user = await get_user.asyncio(
            username=self.username(user_id),
            client=client,
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

    async def get_token(self) -> str:
        async with Client(base_url=self._config.url) as client:
            login_data = BodyAdminTokenApiAdminTokenPost(
                username=self._config.username,
                password=self._config.password,
            )
            token_response = await admin_token.asyncio(client=client, body=login_data)
            access_token = token_response.access_token
            return access_token

    async def get_client(self) -> AuthenticatedClient:
        token = await self.get_token()
        return AuthenticatedClient(base_url=self._config.url, token=token)
