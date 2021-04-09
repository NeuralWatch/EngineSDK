from fastapi import APIRouter, BackgroundTasks, Body, Depends
from starlette.responses import StreamingResponse

from enginesdk.v1.schemas.secrets import Secrets
from enginesdk.config import get_secrets
from enginesdk.v1.services.engineroom import submit_prediction


class Router:
    def __init__(self, predictor):
        self.router = APIRouter()

        async def async_predict_flow(gid: str = None, input: predictor.Input = None):
            output = predictor.run(input)
            submit_prediction(gid=gid, output=output)
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
        ):
            """Asynchronous prediction endpoint.
            This method responds with a status 200, then runs the prediction as
            a background job. The result is sent via callback to the web back-end."""
            background_tasks.add_task(async_predict_flow, gid=gid, input=input)
            return {"status": 200}
