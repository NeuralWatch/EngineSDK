import os
import logging
import yaml

import google.cloud.logging
from fastapi import FastAPI

from enginesdk.v1.routers import docs, health, predict, info


class EngineAPI:
    def __init__(self, predictor, input, output, factory):
        """
        Instantiates a FastAPI application with pre-configured
        routes and services for AI Engines.
        The constructor expects the following kwargs:
        - predictor: object inheriting from services.predict.BasePredictor
        - input: pydantic model for  the AI Engine's input
        - output: pydantic model for  the AI Engine's output
        - factory: object responding to a `mock_input` instance method producing an input sample
        """
        self._set_cloud_logging()

        self.api = self._create_api(
            predictor=predictor,
            input=input,
            output=output,
            factory=factory,
            settings=self._load_settings(),
        )

    def _create_api(self, predictor, factory, input, output, settings):
        title_detail = os.getenv("PROJECT_ID", "Local")
        title = f"{settings.get('name', 'API')}: {title_detail}"
        version = os.getenv("SHORT_SHA", "local")

        api = FastAPI(
            title=title,
            version=version,
            docs_url=None,
            redoc_url=None,
            openapi_url="/v1/openapi.json",
        )

        api.include_router(health.Router().router)

        # /v1
        api_v1_prefix = "/v1"
        api.include_router(
            predict.Router(
                input_type=input, predictor=predictor, predict_factory=factory
            ).router,
            prefix=api_v1_prefix,
        )
        api.include_router(docs.Router().router, prefix=api_v1_prefix)
        api.include_router(
            info.Router(input=input, output=output, settings=settings).router,
            prefix=api_v1_prefix,
        )
        return api

    def _load_settings(self):
        """
        Sets environment variables and loads an `engine.yaml` file if it exists.
        Makes its contents accessible in the engine as env variables, as well as
        to the outside via the /info router.
        """
        os.environ["TZ"] = "UTC"

        try:
            with open("engine.yaml", "r") as stream:
                settings = yaml.safe_load(stream)
                for key, value in settings.items():
                    if not os.getenv(key.upper()):
                        os.environ[key.upper()] = value
                logging.info("engine.yaml successfully loaded.")
                return settings
        except FileNotFoundError:
            logging.warning("engine.yaml not found.")
            return {}

    def _set_cloud_logging(self):
        # If running in a Project, Cloud Run or Cloud Build
        if os.getenv("PROJECT_ID"):
            client = google.cloud.logging.Client()
            client.get_default_handler()
            client.setup_logging()
