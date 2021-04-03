import os

from fastapi import APIRouter


class Router:
    def __init__(self, predictor, options):
        self.router = APIRouter()

        @self.router.get("/schema")
        def get_schema():
            """
            Endpoint for the engine room to obtain the I/O Schema.
            (will be replaced by the /info route)
            """

            return {
                "input": predictor.Input.schema(),
                "output": predictor.Output.schema(),
            }

        @self.router.get("/info")
        def get_info():
            """
            Endpoint for the engine room to obtain the engine's information
            """

            return {
                "engine": {k.lower(): v for k, v in options.items()},
                "schema": {
                    "input": predictor.Input.schema(),
                    "output": predictor.Output.schema(),
                },
            }
