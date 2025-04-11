from pydantic import BaseModel, Field
from typing import List, Optional

class Image(BaseModel):
    image_url: str = Field(..., description="The url of the image")
    image_description: str = Field(..., description="The description content of the image")
    image_resolution: str = Field(..., description="The resolution of the image in pixels")
    is_background: bool = Field(..., description="Whether the image should be used as a background image")

class Images(BaseModel):
    images: List[Image] = Field([], description="List of images with description and resolution")

