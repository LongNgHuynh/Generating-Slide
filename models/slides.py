from pydantic.v1 import BaseModel, Field
from typing import List

class Slide(BaseModel):
    slide_number: int = Field(..., description="The number of the slide in the presentation")
    title: str = Field(..., description="The cutting or summary title of the slide")
    title_description: str = Field(..., description="The description of the slide title")
    body: str = Field(..., description="The detailed content of the slide in markdown format (e.g., headings, bullets, tables")
    layout_description: str = Field(..., description="The layout description of the slide")
    slide_images: List[str]

class Presentation(BaseModel):
    name: str = Field(..., description="The name of the presentation")
    slides: List[Slide] = Field([], description="List of slides in the presentation")
