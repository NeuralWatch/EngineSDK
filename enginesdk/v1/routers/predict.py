import io
import json
import logging
import os
from urllib import parse, request

from fastapi import APIRouter, BackgroundTasks, Body
from starlette.responses import StreamingResponse


class Router:
    def __init__(self, input_type, predictor, predict_factory):
        self.router = APIRouter()

        def callback(gid: str, output=None):
            data = json.dumps(
                {"type": "prediction.success", "gid": gid, "output": output.dict()}
            ).encode("ascii")
            req = request.Request(os.getenv("CALLBACK_URL"), data=data)
            resp = request.urlopen(req)

        async def predict_flow(gid: str = None, input: input_type = None):
            output = predictor.run(input)
            if gid:
                callback(gid=gid, output=output)
            return output

        @self.router.post("/predict/", status_code=200)
        def predict_sync(
            input: input_type = Body(..., example=predict_factory.mock_input()),
        ):
            """Synchronous prediction endpoint.
            In the absence of a `gid`, the prediction is made synchronously and
            the results are sent as a response to the request."""
            return predictor.run(input)

        @self.router.post("/predict/{gid}", status_code=200)
        async def predict_async(
            gid: str,
            background_tasks: BackgroundTasks,
            input: input_type = Body(..., example=predict_factory.mock_input()),
        ):
            """Asynchronous prediction endpoint.
            This method response with a status 200, then runs the prediction as\
            a background job. The result is sent via callback to the web back-end."""
            background_tasks.add_task(predict_flow, gid=gid, input=input)
            return {"status": 200}
