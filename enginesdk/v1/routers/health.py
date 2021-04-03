import json
import os
from urllib import request
from datetime import datetime

from fastapi import APIRouter, Depends

from enginesdk.config import Settings, get_settings


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
                "version": settings.revision,
                "time": datetime.utcnow(),
            }
            return response

        @self.router.post("/deployed")
        def trigger_deployed_hook(
            settings: Settings = Depends(get_settings),
        ):
            """
            Trigger the `deployed` hook, which registers this API to the engine room.
            """

            data = json.dumps(
                {"type": "engine.deployed", "engine_slug": settings.engine_slug}
            ).encode("ascii")
            req = request.Request(settings.callback_url, data=data)
            return request.urlopen(req)
