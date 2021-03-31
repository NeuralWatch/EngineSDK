import os

import google.cloud.logging
from fastapi import FastAPI

from enginesdk.v1.routers import docs, health, predict, schemas


class EngineAPI:
    def __init__(self, predictor, factory, input, output, title):
        os.environ["TZ"] = "UTC"
        title_detail = os.getenv("PROJECT_ID", "Local")
        version = os.getenv("SHORT_SHA", "local")

        client = google.cloud.logging.Client()
        client.get_default_handler()
        client.setup_logging()

        self.api = FastAPI(
            title=f"{title}: {title_detail}",
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
            schemas.Router(input=input, output=output).router, prefix=api_v1_prefix
        )