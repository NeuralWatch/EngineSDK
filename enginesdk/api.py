import os
import logging

import google.cloud.logging
from fastapi import FastAPI

from enginesdk.v1.routers import docs, health, predict, info
from enginesdk.config import get_settings
from enginesdk.v1.services.engineroom import broadcast_online_status

# Broadcast engine's online status to the Engine Room
broadcast_online_status()


class EngineAPI:
    def __init__(self, predictor):
        """Instantiates a FastAPI application with pre-configured routes and services for AI Engines.
        The constructor expects a predictor object inheriting from services.predict.BasePredictor."""
        os.environ["TZ"] = "UTC"

        self.settings = get_settings()
        self._set_cloud_logging()

        self.api = self._create_api(
            predictor=predictor,
        )

    def _create_api(self, predictor):
        title = f"{self.settings.ENGINE_NAME}: {os.getenv('PROJECT_ID', 'Local')}"

        api = FastAPI(
            title=title,
            version=self.settings.REVISION,
            docs_url=None,
            redoc_url=None,
            openapi_url="/v1/openapi.json",
        )

        api.include_router(health.Router().router)

        # /v1
        api_v1_prefix = "/v1"
        api.include_router(
            predict.Router(predictor=predictor).router,
            prefix=api_v1_prefix,
        )
        api.include_router(docs.Router().router, prefix=api_v1_prefix)
        api.include_router(
            info.Router(predictor=predictor).router,
            prefix=api_v1_prefix,
        )
        return api

    def _set_cloud_logging(self):
        # If running in a Project, Cloud Run or Cloud Build
        if os.getenv("PROJECT_ID"):
            client = google.cloud.logging.Client()
            client.get_default_handler()
            client.setup_logging()
