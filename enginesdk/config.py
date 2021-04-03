import logging
import os
import sys
import time
from functools import lru_cache

from pydantic import BaseSettings
from fastapi.security import OAuth2PasswordBearer
from google.cloud import secretmanager_v1beta1 as secretmanager
from google.cloud import storage

from enginesdk.v1.schemas.secrets_config import SecretsConfig


class Settings(BaseSettings):
    engine_slug: str = os.getenv("ENGINE_SLUG")
    callback_url: str = os.getenv("CALLBACK_URL")
    project_id: str = os.getenv("PROJECT_ID", "Local")
    revision: str = os.getenv("SHORT_SHA", "local")


settings = Settings()


@lru_cache()
def get_settings():
    return Settings()


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
    def build_secrets_config(project_id: str = "") -> SecretsConfig:
        result = SecretsConfig()
        if not project_id:
            return result
        for secret_id in result.dict().keys():
            version_path = secrets_client.secret_version_path(
                project_id, secret_id, "latest"
            )
            secret_version = secrets_client.access_secret_version(version_path)
            secret_data = secret_version.payload.data.decode("UTF-8")
            setattr(result, secret_id, secret_data)
        return result


c = Config()
logger = c.get_logger()
project_id = os.getenv("PROJECT_ID")

# if running in a project, cloud run or cloud build
if project_id:
    gcs_client = storage.Client(project=project_id)
    secrets_client = secretmanager.SecretManagerServiceClient()
    apisecrets = c.build_secrets_config(project_id)

# if running locally
else:
    apisecrets = c.build_secrets_config()
    #     GCLOUD_CONFIG_PROJECT_ID = (
    #         os.popen("gcloud config get-value project").read().strip()
    #     )
    #     gcs_client = storage.Client(project=GCLOUD_CONFIG_PROJECT_ID)
    # secrets_client = secretmanager.SecretManagerServiceClient()
