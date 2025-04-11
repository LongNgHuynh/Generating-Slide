from pydantic import BaseModel, Field
from typing import List

class Slide(BaseModel):
    slide_number: int = Field(..., description="The number of the slide in the presentation")
    title: str = Field(..., description="The cutting or summary title of the slide, eg: Introduction, Conclusion, etc.")
    body: str = Field(..., description="The detailed content of the slide in markdown format (e.g., headings, bullets, tables")
    layout_description: str = Field(..., description="The layout description of the slide")
    slide_images: List[str]

class Presentation(BaseModel):
    name: str = Field(..., description="The name of the presentation")
    image_background: str = Field(None, description="The image url of the background of the presentation, if none provided url, return None")
    slides: List[Slide] = Field(..., description="List of slides in the presentation")
