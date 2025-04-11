import requests
from io import BytesIO
import json
import os
import sys

# Add the project root directory to Python path
current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_directory)

from models.visualize_slides import VisualizeSlides, VisualizeSlide
from langchain_core.tools import tool
from models.LLMs import GPT_o3

llm = GPT_o3(reasoning_effort="high")

def create_slides(presentation: dict) -> dict:
    """Create a slides based on the given presentation."""
    # Read the rules.txt file
    rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rules", "slide_rules.txt")
    with open(rules_path, "r", encoding="utf-8") as f:
        rules_content = f.read()
    
    prompt = f"""
    {rules_content}
    
    You are an expert in Marpit Markdown, a presentation slide deck format that maintains compatibility with standard Markdown viewers.
    You need to think step by step, and create a slides based on the outline.
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
    
    IMPORTANT: Your response must be structured as a VisualizeSlides object with:
    1. A 'presentation_content' field that is a list of VisualizeSlide objects
    2. Each VisualizeSlide object must have a 'slide_content' field containing the html content for that slide
    3. A 'style' field containing the CSS styling for the slides
    
    This is a presentation outline:
    {presentation}
    """
    
    structured_llm = llm.with_structured_output(VisualizeSlides)
    slides = structured_llm.invoke(prompt)
    
    print("Creating slides...")

    return slides

if __name__ == "__main__":
    with open("./examples/presentation.json", "r", encoding="utf-8") as f:
        presentation = json.load(f)
    slides = create_slides(presentation=presentation)
    # Access the attributes of the VisualizeSlides object
    slide_content = [slide.slide_content for slide in slides.presentation_content]
    css = slides.style
    print(slide_content)
    print(css)