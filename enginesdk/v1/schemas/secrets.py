from os import getenv
from pydantic import BaseModel
from dotenv import load_dotenv

# TODO: Remove this and override ENVs in test_api.py
load_dotenv("test.env")


class Secrets(BaseModel):
    SECRET_KEY: str = getenv("MAIN_API_KEY")
    CALLBACK_URL: str = getenv("CALLBACK_URL")
    CLOUDINARY_URL: str = getenv("CLOUDINARY_URL")
