import os

from fastapi import APIRouter


class Router:
    def __init__(self, input, output, settings):
        self.router = APIRouter()

        @self.router.get("/schema")
        def get_schema():
            """
            Endpoint for the engine room to obtain the I/O Schema.
            (will be replaced by the /info route)
            """

            return {"input": input.schema(), "output": output.schema()}

        @self.router.get("/info")
        def get_info():
            """
            Endpoint for the engine room to obtain the engine's information
            """

            return {
                "engine": settings,
                "schema": {
                    "input": input.schema(),
                    "output": output.schema(),
                },
            }
