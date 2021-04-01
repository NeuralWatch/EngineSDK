from os import getenv

from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKey
from starlette.responses import JSONResponse

from enginesdk.v1.services.auth import AuthService


class Router:
    def __init__(self):
        self.router = APIRouter()
        self.auth_service = AuthService()
        self.API_KEY_NAME = getenv("API_KEY_NAME", "access_token")
        self.COOKIE_DOMAIN = getenv("COOKIE_DOMAIN")

        @self.router.get("/openapi.json", include_in_schema=False)
        async def get_open_api_endpoint(
            api_key: APIKey = Depends(self.auth_service.authenticate_admin),
        ):
            response = JSONResponse(
                get_openapi(title="AI Engine API", version=1, routes=self.router.routes)
            )
            return response

        @self.router.get("/docs", tags=["Documentation"])
        async def get_documentation(
            api_key: APIKey = Depends(self.auth_service.authenticate_admin),
        ):
            response = get_swagger_ui_html(openapi_url="/v1/openapi.json", title="docs")
            response.set_cookie(
                self.API_KEY_NAME,
                value=api_key,
                domain=self.COOKIE_DOMAIN,
                httponly=True,
                max_age=1800,
                expires=1800,
            )
            return response
