import os
from urllib import request
from datetime import datetime

from fastapi import APIRouter, Depends

from enginesdk.v1.schemas.settings import Settings
from enginesdk.config import get_settings


class Router:
    def __init__(self):
        self.router = APIRouter()

        @self.router.get("/healthcheck", tags=["public"])
        def healthcheck(settings: Settings = Depends(get_settings)):
            """Check if API is online."""
            response = {
                "message": "Service online",
                "version": settings.REVISION,
                "time": datetime.utcnow(),
            }
            return response
