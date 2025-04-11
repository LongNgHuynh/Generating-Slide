from models.visualize_slides import VisualizeSlides, VisualizeSlide
from langchain_core.tools import tool
from models.LLMs import GPT_o3
import os

llm = GPT_o3(reasoning_effort="high")

def enhance_slides_positions(slides: list, css: str) -> VisualizeSlides:
    """Enhance the positions of the slides."""
    rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rules", "image_rules.txt")
    with open(rules_path, "r", encoding="utf-8") as f:
        rules_content = f.read()
    
    prompt = f"""
    {rules_content}
    
    You are an expert in using bootstrap classes to style and position elements in markdown.
    You will be given a list of slides with their content and images.
    You will need to enhance the positions of the slides to make them more visually appealing.
    
    The image_background should set as a background image for all slides, means it should use opacity and layer it in back of the slide.
    Each slide must be responsive. the image should be in slide and in proper size to balance with text.
    
    Return in marp file using html and bootstrap classes.
    
    IMPORTANT: Your response must be structured as a VisualizeSlides object with:
    1. A 'presentation_content' field that is a list of VisualizeSlide objects
    2. Each VisualizeSlide object must have a 'slide_content' field containing the html content for that slide
    3. A 'style' field containing the CSS styling for the slides
    
    This is slide content:
    {slides}

    This is css:
    {css}
    """
    
    structured_llm = llm.with_structured_output(VisualizeSlides)
    enhanced_slides = structured_llm.invoke(prompt)
    
    print("Enhancing slide positions...")

    return enhanced_slides