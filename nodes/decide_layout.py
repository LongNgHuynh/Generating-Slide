from models.slides import Presentation
from langchain_core.tools import tool
from models.LLMs import GPT_4o, GPT_o3
import requests
from io import BytesIO
import json

llm = GPT_o3()

def decide_layout(outline: dict, image_descriptions: dict) -> dict:
    """Create a layout based on the given content."""
    prompt = f"""
    You are an expert in presentation design and layout.
    
    I need you to create a detailed layout description for each slide in this presentation.
    For each slide, provide a specific layout description that includes:
    - The position of the title, content, and images in various types of slides (e.g. on the right or left or center or top or bottom, in vertical or horizontal dimension, in the center or in the edge, etc.).
    - The size and proportions of each element.
    - Any specific styling or visual hierarchy.

    
    The layout description should be clear and detailed enough for a designer to implement.
    
    Here is the presentation outline:
    {outline}
    
    
    
    Here are the image descriptions, you need to decide 1 image for each slide, and only 1 image for all background in presentation:
    {image_descriptions}
    
    IMPORTANT: You must provide a non-empty layout_description for each slide.
    NOTICE: Do not make one slide the same layout as previous or after slide.
    """
    
    # First, get the layout descriptions
    layout_response = llm.invoke(prompt)
    
    # Now create a properly structured presentation with the layout descriptions
    structured_prompt = f"""
    Create a presentation with the following content and layout descriptions.
    Make sure each slide has a non-empty layout_description field.
    
    Content and layout:
    {layout_response}
    """
    
    structured_llm = llm.with_structured_output(Presentation)
    presentation = structured_llm.invoke(structured_prompt)
    
    # Ensure all slides have a layout_description
    if hasattr(presentation, 'slides'):
        for slide in presentation.slides:
            if not slide.layout_description or slide.layout_description.strip() == "":
                slide.layout_description = "Default layout with title at top, content on the right, and images on the left."
    
    return presentation
