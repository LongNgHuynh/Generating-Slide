from models.visualize_slides import VisualizeSlides
from langchain_core.tools import tool
from models.LLMs import GPT_o3
import requests
from io import BytesIO
import json
import os

llm = GPT_o3()

def enhance_slides_positions(slides: dict, css: dict) -> dict:
    """Enhance the positions of the slides."""
    rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rules", "image_rules.txt")
    with open(rules_path, "r") as f:
        rules_content = f.read()
    
    prompt = f"""
    {rules_content}
    
    You are an expert in css styling and positioning of elements in markdown.
    You will be given a list of slides with their content and images.
    You will need to enhance the positions of the slides to make them more visually appealing.
    
    This is slide content:
    {slides}

    This is css:
    {css}
    """
    
    structured_llm = llm.with_structured_output(VisualizeSlides)
    slides = structured_llm.invoke(prompt)
    
    print(slides)

    return slides