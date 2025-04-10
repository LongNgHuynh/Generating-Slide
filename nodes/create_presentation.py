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

# def download_image(url: str, save_path: Optional[Path] = None) -> BytesIO:
#     """
#     Download image from URL with retry mechanism and optional saving.
    
#     Args:
#         url: Image URL to download
#         save_path: Optional path to save the image
    
#     Returns:
#         BytesIO object containing the image data
#     """
#     for attempt in range(MAX_RETRIES):
#         try:
#             response = requests.get(url, timeout=TIMEOUT)
#             response.raise_for_status()
#             image_content = BytesIO(response.content)
            
#             if save_path:
#                 save_path.parent.mkdir(parents=True, exist_ok=True)
#                 with open(save_path, 'wb') as f:
#                     f.write(image_content.getvalue())
            
#             return image_content
            
#         except requests.exceptions.RequestException as e:
#             if attempt == MAX_RETRIES - 1:
#                 logger.error(f"Failed to download image from {url}: {str(e)}")
#                 raise
#             continue

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
        
        # saved_images = []
        # for idx, img_url in enumerate(img_src_list):
        #     try:
        #         safe_title = "".join(c if c.isalnum() else "_" for c in slide["title"])
        #         filename = f"{safe_title}_{idx}.jpg"
        #         save_path = DATA_DIR / filename
                
        #         download_image(img_url, save_path)
        #         saved_images.append(str(save_path))
                
        #     except Exception as e:
        #         logger.error(f"Failed to process image {img_url}: {str(e)}")
        #         continue
                
        # return saved_images
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
        for slide in outline["slides"]:
            slide["slide_images"] = process_slide_images(slide, searcher)
    
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

if __name__ == "__main__":
    try:
        presentation = create_presentation("Artificial Intelligence Basics")
        print(presentation)
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")