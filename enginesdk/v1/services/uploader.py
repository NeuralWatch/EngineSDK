import re
from os import getenv
import cloudinary
from enginesdk.config import get_settings, get_secrets


def _cloudinary_upload(filename, **options):
    settings = get_settings()
    secrets = get_secrets()

    credentials = re.match(
        r"^cloudinary://(?P<api_key>\d+):(?P<api_secret>[a-zA-Z\d]+)@(?P<cloud_name>[a-z\d]+)",
        secrets.CLOUDINARY_URL,
    ).groupdict()
    cloudinary.config(**credentials)

    SLUG = settings.ENGINE_SLUG
    BRANCH_NAME = getenv("BRANCH_NAME", "debug")

    options = {
        "folder": f"kaepler/engines/{SLUG}",
        "tag": f"{SLUG},{BRANCH_NAME}",
        **options,
    }

    return cloudinary.uploader.upload(filename, **options)


def upload(filename, service="cloudinary", **options):
    # if service == "google-cloud":
    #     return _google_cloud_upload()

    return _cloudinary_upload(filename, **options)