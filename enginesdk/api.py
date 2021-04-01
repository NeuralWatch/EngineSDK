import os
import logging
import yaml

import google.cloud.logging
from fastapi import FastAPI

from enginesdk.v1.routers import docs, health, predict, info


class EngineAPI:
    def __init__(self, predictor, factory, input, output):
        settings = self._load_settings()

        os.environ["TZ"] = "UTC"
        title_detail = os.getenv("PROJECT_ID", "Local")
        title = f"{settings.get('name', 'API')}: {title_detail}"
        version = os.getenv("SHORT_SHA", "local")

        client = google.cloud.logging.Client()
        client.get_default_handler()
        client.setup_logging()

        self.api = FastAPI(
            title=title,
            version=version,
            docs_url=None,
            redoc_url=None,
            openapi_url="/v1/openapi.json",
        )

        self.api.include_router(health.Router().router)

        # /v1
        api_v1_prefix = "/v1"
        self.api.include_router(
            predict.Router(
                input_type=input, predictor=predictor, predict_factory=factory
            ).router,
            prefix=api_v1_prefix,
        )
        self.api.include_router(docs.Router().router, prefix=api_v1_prefix)
        self.api.include_router(
            info.Router(input=input, output=output, settings=settings).router,
            prefix=api_v1_prefix,
        )

    def _load_settings(self):
        """
        Loads an `engine.yaml` file if it exists and makes its contents accessible
        in the engine as env variables, as well as to the outside via the /info route.
        """
        try:
            with open("engine.yaml", "r") as stream:
                settings = yaml.safe_load(stream)
                for key, value in settings.items():
                    if not os.environ[key.upper()]:
                        os.environ[key.upper()] = value
                logging.info("engine.yaml successfully loaded.")
                return settings
        except FileNotFoundError:
            logging.warning("engine.yaml not found.")
            return {}
