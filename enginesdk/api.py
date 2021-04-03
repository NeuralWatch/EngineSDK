import os
import logging
import yaml

import google.cloud.logging
from fastapi import FastAPI

from enginesdk.v1.routers import docs, health, predict, info
from enginesdk.config import settings


class EngineAPI:
    def __init__(self, predictor):
        """
        Instantiates a FastAPI application with pre-configured routes and services for AI Engines.
        The constructor expects a predictor object inheriting from services.predict.BasePredictor.
        """
        self._set_cloud_logging()

        options = self._load_options()

        self.api = self._create_api(
            predictor=predictor,
            options=options,
        )

    def _create_api(self, predictor, options):
        title = f"{options.get('name', 'API')}: {settings.project_id}"

        api = FastAPI(
            title=title,
            version=settings.revision,
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
            info.Router(predictor=predictor, options=options).router,
            prefix=api_v1_prefix,
        )
        return api

    def _load_options(self):
        """
        Sets environment variables and loads an `engine.yaml` file if it exists.
        Makes its contents accessible in the engine as env variables, as well as
        to the outside via the /info router.
        """
        os.environ["TZ"] = "UTC"

        try:
            with open("engine.yaml", "r") as stream:
                options = yaml.safe_load(stream)
                for key, value in options.items():
                    if not os.getenv(str(key.upper())):
                        os.environ[str(key.upper())] = str(value)
                logging.info("engine.yaml successfully loaded.")
                return options
        except FileNotFoundError:
            logging.warning("engine.yaml not found.")
            return {}

    def _set_cloud_logging(self):
        # If running in a Project, Cloud Run or Cloud Build
        if os.getenv("PROJECT_ID"):
            client = google.cloud.logging.Client()
            client.get_default_handler()
            client.setup_logging()
