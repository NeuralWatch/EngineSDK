from pydantic import BaseModel


class ImageUrl(BaseModel):
    image_url: str


class VideoUrl(BaseModel):
    video_url: str
