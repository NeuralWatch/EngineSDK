import os
from fastapi import APIRouter, Depends
from enginesdk.v1.schemas.settings import Settings
from enginesdk.v1.schemas.secrets import Secrets
from enginesdk.config import get_settings, get_secrets
from enginesdk.v1.services.engineroom import broadcast_online_status


class Router:
    def __init__(self, predictor):
        self.router = APIRouter()

        @self.router.get("/broadcast")
        def broadcast(
            settings: Settings = Depends(get_settings),
            secrets: Secrets = Depends(get_secrets),
        ):
            """Triggers the `online` hook, which notifies to the engine room that this API is online."""

            return broadcast_online_status(settings, secrets)

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
