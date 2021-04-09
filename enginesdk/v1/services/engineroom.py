import json
from urllib import request
from enginesdk.v1.schemas.secrets import Secrets
from enginesdk.v1.schemas.settings import Settings
from enginesdk.config import get_secrets, get_settings


def broadcast_online_status(
    settings: Settings = get_settings(), secrets: Secrets = get_secrets()
):
    """Triggers the `online` hook, which notifies to the engine room that this API is online."""

    data = json.dumps(
        {
            "type": "engine.online",
            "engine_slug": settings.ENGINE_SLUG,
            "service_url": settings.SERVICE_URL,
            "version": settings.VERSION,
            "revision": settings.REVISION,
        }
    ).encode("ascii")

    req = request.Request(secrets.CALLBACK_URL, data=data)
    return request.urlopen(req)


def submit_prediction(
    gid: str, url: str = None, output=None, secrets: Secrets = get_secrets()
):
    """Submits the result of the prediction to the engine room."""

    data = json.dumps(
        {"type": "prediction.success", "gid": gid, "output": output.dict()}
    ).encode("ascii")

    req = request.Request(url or secrets.CALLBACK_URL, data=data)
    return request.urlopen(req)