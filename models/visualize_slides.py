from pydantic.v1 import BaseModel, Field
from typing import List, Optional

class VisualizeSlide(BaseModel):
    slide_content: str = Field(..., description="The content of the slide in markdown format")

class VisualizeSlides(BaseModel):
    presentation_content: List[VisualizeSlide] = Field(..., description="List of slides in the presentation")
    style: Optional[str] = Field(None, description="The style of the presentation in css format")
