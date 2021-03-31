import os
from datetime import datetime

from fastapi import APIRouter


class Router:
    def __init__(self):
        self.router = APIRouter()

        @self.router.get("/healthcheck", tags=["public"])
        def healthcheck():
            """
            Check if API is online.
            """
            message = "Service online"
            version = os.getenv("SHORT_SHA", "local")
            response = {
                "message": message,
                "version": version,
                "time": datetime.utcnow(),
            }
            return response
