import logging
from os import getenv, popen
import sys
import time
import yaml
from functools import lru_cache

from fastapi.security import OAuth2PasswordBearer
from google.cloud import secretmanager_v1beta1 as secretmanager
from google.cloud import storage

from enginesdk.v1.schemas.secrets import Secrets
from enginesdk.v1.schemas.settings import Settings


class Config:
    @staticmethod
    def get_logger(level: int = logging.INFO) -> logging.Logger:
        tz = time.strftime("%z")
        logging.config = logging.basicConfig(
            format=(
                f"[%(asctime)s.%(msecs)03d {tz}] "
                "[%(process)s] [%(pathname)s L%(lineno)d] "
                "[%(levelname)s] %(message)s"
            ),
            level=level,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger = logging.getLogger(__name__)
        return logger

    @staticmethod
    def build_settings() -> Settings:
        return Settings()

    @staticmethod
    def build_secrets(project_id: str = "") -> Secrets:
        result = Secrets()
        if project_id:
            for secret_id, secret_data in result.dict().items():
                if not secret_data:
                    # Only load cloud secrets if ENV is not set (allows override)
                    version_path = secrets_client.secret_version_path(
                        project_id, secret_id, "latest"
                    )
                    secret_version = secrets_client.access_secret_version(version_path)
                    secret_data = secret_version.payload.data.decode("UTF-8")
                setattr(result, secret_id, secret_data)
        return result


c = Config()
logger = c.get_logger()
project_id = (
    # if running in a project, cloud run or cloud build
    getenv("PROJECT_ID")
    # if running locally (TODO: handle case when no local project found)
    or popen("gcloud config get-value project").read().strip()
)

if project_id:
    gcs_client = storage.Client(project=project_id)
    secrets_client = secretmanager.SecretManagerServiceClient()


@lru_cache()
def get_settings():
    return c.build_settings()


@lru_cache()
def get_secrets():
    return c.build_secrets(project_id)