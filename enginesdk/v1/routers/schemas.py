import json
import os
from urllib import request

from fastapi import APIRouter


class Router:
    def __init__(self, input, output):
        self.router = APIRouter()

        @self.router.post("/deployed")
        def trigger_deployed_hook():
            "Trigger the `deployed` hook, which registers this API to the engine room."

            data = json.dumps(
                {"type": "engine.deployed", "engine_slug": os.getenv("ENGINE_SLUG")}
            ).encode("ascii")
            req = request.Request(os.getenv("CALLBACK_URL"), data=data)
            return request.urlopen(req)

        @self.router.get("/schema")
        def read_schema():
            "Endpoint for the engine room to obtain the I/O Schema"

            return {"input": input.schema(), "output": output.schema()}
