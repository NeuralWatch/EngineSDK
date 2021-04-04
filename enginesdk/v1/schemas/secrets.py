from os import getenv
from pydantic import BaseModel


class Secrets(BaseModel):
    SECRET_KEY: str = getenv("MAIN_API_KEY")
    CALLBACK_URL: str = getenv("CALLBACK_URL")
    CLOUDINARY_URL: str = getenv("CLOUDINARY_URL")
