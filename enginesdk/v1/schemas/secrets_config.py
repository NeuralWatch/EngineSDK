from os import getenv

from pydantic import BaseModel


class SecretsConfig(BaseModel):
    PROJECT_ID: str = None
    SECRET_KEY: str = getenv("MAIN_API_KEY")
