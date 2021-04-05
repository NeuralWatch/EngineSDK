import os
from fastapi import APIRouter, Depends
from enginesdk.v1.schemas.settings import Settings
from enginesdk.config import get_settings


class Router:
    def __init__(self, predictor):
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
        def get_info(
            settings: Settings = Depends(get_settings),
        ):
            """
            Endpoint for the engine room to obtain the engine's information
            """

            return {
                "settings": {
                    k.lower(): settings.__dict__[k] for k in settings.__dict__
                },
                "schema": {
                    "input": predictor.Input.schema(),
                    "output": predictor.Output.schema(),
                },
            }
