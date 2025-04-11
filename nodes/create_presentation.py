from pathlib import Path
from typing import List, Dict, Optional
from models.slides import Presentation
from langchain_core.tools import tool
from models.LLMs import GPT_4o
import requests
from io import BytesIO
from utils.search import Searxng
import json
import logging
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = GPT_4o()

# Constants
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
MAX_RETRIES = 3
TIMEOUT = 10

def extract_img_src(images_url: List[Dict]) -> List[str]:
    """
    Extract image source URLs from search results.
    
    Args:
        images_url: List of dictionaries containing image search results
    
    Returns:
        List of image URLs
    """
    return [item["img_src"] for item in images_url if "img_src" in item]

def process_slide_images(slide: Dict, searcher: Searxng) -> List[str]:
    """
    Process images for a single slide.
    
    Args:
        slide: Slide dictionary containing title and body
        searcher: Searxng instance for image search
    
    Returns:
        List of local image paths
    """
    try:
        search_query = f"{slide['title']}\n{slide['body']}"
        images_url = json.loads(
            searcher.image_search(search_query, max_results=1)
        )["results"]
        img_src_list = extract_img_src(images_url)
        
        return img_src_list
    
    except Exception as e:
        logger.error(f"Failed to search images for slide '{slide['title']}': {str(e)}")
        return []

def add_image_to_outline(outline: dict) -> dict:
    """
    Add images to presentation outline.
    
    Args:
        outline: Presentation outline dictionary
    
    Returns:
        Updated outline with local image paths
    """
    searcher = Searxng(images=True)
    
    if "slides" in outline:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Map each slide to its future and maintain original order
            future_to_slide = {
                executor.submit(process_slide_images, slide, searcher): i 
                for i, slide in enumerate(outline["slides"])
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_slide):
                slide_index = future_to_slide[future]
                outline["slides"][slide_index]["slide_images"] = future.result()
    
    return outline


def create_presentation(topic: str) -> dict:
    """
    Create a presentation with structured slides and images based on the given topic.
    
    Args:
        topic: Presentation topic
    
    Returns:
        Presentation object with slides and images
    """
    prompt = f"""Create a presentation about {topic}.
    The presentation should include:
    - A slide title
    - Content slides with clear headings and bullet points
    
    There should be a welcome slide at the beginning, table of contents slide which has all section title (contains introduction sections first, comes to others sections, then conclusion at the end),
    an overview slide, and a conclusion slide at the end.
    Do not include any image_instruction or layout_instruction, let it null for processing on the next step.
    Format the content using markdown for better readability.
    """
    
    try:
        structured_llm = llm.with_structured_output(Presentation)
        presentation = structured_llm.invoke(prompt)
        
        presentation_with_images = add_image_to_outline(json.loads(presentation.json()))
        return presentation_with_images
        
    except Exception as e:
        logger.error(f"Failed to create presentation: {str(e)}")
        raise