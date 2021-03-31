import json
import os
from urllib import request
from datetime import datetime

from fastapi import APIRouter


class Router:
    def __init__(self):
        self.router = APIRouter()

        @self.router.get("/healthcheck", tags=["public"])
        def healthcheck():
            """
            Check if API is online.
            """
            message = "Service online"
            version = os.getenv("SHORT_SHA", "local")
            response = {
                "message": message,
                "version": version,
                "time": datetime.utcnow(),
            }
            return response

        @self.router.post("/deployed")
        def trigger_deployed_hook():
            """
            Trigger the `deployed` hook, which registers this API to the engine room.
            """

            data = json.dumps(
                {"type": "engine.deployed", "engine_slug": os.getenv("ENGINE_SLUG")}
            ).encode("ascii")
            req = request.Request(os.getenv("CALLBACK_URL"), data=data)
            return request.urlopen(req)
