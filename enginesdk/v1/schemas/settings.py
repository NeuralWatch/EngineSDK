from os import getenv
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(".settings")


class Settings(BaseModel):
    ENGINE_NAME: str = getenv("ENGINE_NAME", "Kaepler Engine")
    ENGINE_SLUG: str = getenv("ENGINE_SLUG", "kaepler-engine")
    SERVICE_URL: str = getenv("SERVICE_URL")
    VERSION: str = getenv("VERSION", "v1")
    REVISION: str = getenv("SHORT_SHA", "local")
    API_KEY_NAME: str = getenv("API_KEY_NAME", "access_token")
    COOKIE_DOMAIN: str = getenv("COOKIE_DOMAIN", "kaepler.com")
