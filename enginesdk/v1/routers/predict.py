import io
import json
import logging
import os
from urllib import parse, request

from fastapi import APIRouter, BackgroundTasks, Body, Depends
from starlette.responses import StreamingResponse

from enginesdk.v1.schemas.secrets import Secrets
from enginesdk.config import get_secrets


class Router:
    def __init__(self, predictor):
        self.router = APIRouter()

        def callback(gid: str, callback_url: str, output=None):
            data = json.dumps(
                {"type": "prediction.success", "gid": gid, "output": output.dict()}
            ).encode("ascii")
            req = request.Request(callback_url, data=data)
            resp = request.urlopen(req)

        async def async_predict_flow(
            callback_url: str, gid: str = None, input: predictor.Input = None
        ):
            output = predictor.run(input)
            if callback_url:
                callback(gid=gid, callback_url=callback_url, output=output)
            return output

        @self.router.post("/predict", status_code=200)
        def predict_sync(
            input: predictor.Input = Body(..., example=predictor.factory.mock_input()),
        ):
            """Synchronous prediction endpoint.
            In the absence of a `gid`, the prediction is made synchronously and
            the results are sent as a response to the request."""
            return predictor.run(input)

        @self.router.post("/predict/{gid}", status_code=200)
        async def predict_async(
            gid: str,
            background_tasks: BackgroundTasks,
            input: predictor.Input = Body(..., example=predictor.factory.mock_input()),
            secrets: Secrets = Depends(get_secrets),
            callback_url: str = None,
        ):
            """Asynchronous prediction endpoint.
            This method responds with a status 200, then runs the prediction as
            a background job. The result is sent via callback to the web back-end."""
            background_tasks.add_task(
                async_predict_flow,
                callback_url=callback_url or secrets.CALLBACK_URL,
                gid=gid,
                input=input,
            )
            return {"status": 200}
