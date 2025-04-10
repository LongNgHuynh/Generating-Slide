from models.visualize_slides import VisualizeSlides
from langchain_core.tools import tool
from models.LLMs import GPT_4o
import requests
from io import BytesIO
import json
import os

llm = GPT_4o()

def create_slides(presentation: dict) -> dict:
    """Create a slides based on the given presentation."""
    # Read the rules.txt file
    rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rules", "slide_rules.txt")
    with open(rules_path, "r") as f:
        rules_content = f.read()
    
    prompt = f"""
    {rules_content}
    
    You are an expert in Marpit Markdown, a presentation slide deck format that maintains compatibility with standard Markdown viewers.
    You will be given a presentation outline, and you need to create a slides based on the outline.
    The content of 1 slide can be in next slide if 1 slide is not enough, in that next slide, should only contain content that have not been included in the previous slide.
    
    You must also provide CSS styling for the slides that will make them visually appealing and consistent.
    The CSS should include styling for:
    - Headers and text
    - Background colors and images
    - Layout and spacing
    - Lists and bullet points
    - Images and diagrams
    
    Note that do not change text size bigger, only decrease image size if needed.
    
    This is a presentation outline:
    {presentation}
    """
    
    structured_llm = llm.with_structured_output(VisualizeSlides)
    slides = structured_llm.invoke(prompt)
    
    print(slides)

    return slides