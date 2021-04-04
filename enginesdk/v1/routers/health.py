import json
import os
from urllib import request
from datetime import datetime

from fastapi import APIRouter, Depends

from enginesdk.v1.schemas.secrets import Secrets
from enginesdk.v1.schemas.settings import Settings
from enginesdk.config import get_settings, get_secrets


class Router:
    def __init__(self):
        self.router = APIRouter()

        @self.router.get("/healthcheck", tags=["public"])
        def healthcheck(settings: Settings = Depends(get_settings)):
            """
            Check if API is online.
            """
            response = {
                "message": "Service online",
                "version": settings.REVISION,
                "time": datetime.utcnow(),
            }
            return response

        @self.router.post("/deployed")
        def trigger_deployed_hook(
            settings: Settings = Depends(get_settings),
            secrets: Secrets = Depends(get_secrets),
        ):
            """
            Trigger the `deployed` hook, which registers this API to the engine room.
            """

            data = json.dumps(
                {"type": "engine.deployed", "engine_slug": settings.ENGINE_SLUG}
            ).encode("ascii")
            req = request.Request(secrets.CALLBACK_URL, data=data)
            return request.urlopen(req)
