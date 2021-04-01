from os import getenv

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyCookie, APIKeyHeader, APIKeyQuery
from pydantic import UUID4
from starlette import status

from enginesdk.config import apisecrets

SECRET_KEY = apisecrets.SECRET_KEY
API_KEY_NAME = getenv("API_KEY_NAME", "access_token")


class AuthService:
    async def authenticate_admin(
        self,
        api_key_query: str = Security(APIKeyQuery(name=API_KEY_NAME, auto_error=False)),
        api_key_header: str = Security(
            APIKeyHeader(name=API_KEY_NAME, auto_error=False)
        ),
        api_key_cookie: str = Security(
            APIKeyCookie(name=API_KEY_NAME, auto_error=False)
        ),
    ):
        if self._check_admin_apikey(api_key_query):
            return api_key_query
        elif self._check_admin_apikey(api_key_header):
            return api_key_header
        elif self._check_admin_apikey(api_key_cookie):
            return api_key_cookie
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

    @staticmethod
    def _check_admin_apikey(apikey: UUID4) -> UUID4:
        if apikey == SECRET_KEY:
            try:
                apikey = UUID4(apikey)
                return apikey
            except (ValueError, TypeError) as error:
                return None
        else:
            return None
