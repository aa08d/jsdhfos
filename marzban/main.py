from marzban_api_client.models.body_admin_token_api_admin_token_post import BodyAdminTokenApiAdminTokenPost
from marzban_api_client.api.admin import admin_token
from marzban_api_client import Client, AuthenticatedClient


async def get_token(url: str, username: str, password: str) -> str:
    async with Client(base_url=url) as client:
        login_data = BodyAdminTokenApiAdminTokenPost(
            username=username,
            password=password,
        )
        token_response = await admin_token.asyncio(client=client, body=login_data)
        access_token = token_response.access_token
        return access_token


def get_client(url: str, token: str) -> AuthenticatedClient:
    return AuthenticatedClient(base_url=url, token=token)
